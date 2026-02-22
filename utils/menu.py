"""Interactive menu system for AtlasPi"""

import os
import sys
import subprocess
import logging
import threading
import time
import math
import shutil
from utils.config import get_config_paths
from utils.config import load_config
from utils.database import initialize_database
from utils.app import run_application_loop
from utils.common import strings

# Global service state
service_thread = None
service_running = False
stop_service_flag = threading.Event()
planet_animation_active = False
planet_thread = None
planet_stop_flag = threading.Event()

class PlanetRenderer:
    """Simple planet animation renderer"""
    
    def __init__(self, radius=6):
        self.radius = radius
        self.animation_running = False
        
    def supports_ansi(self):
        return sys.stdout.isatty()
        
    def hide_cursor(self):
        if self.supports_ansi():
            sys.stdout.write('\033[?25l')
            sys.stdout.flush()
            
    def show_cursor(self):
        if self.supports_ansi():
            sys.stdout.write('\033[?25h')
            sys.stdout.flush()
            
    def move_cursor_to(self, row, col):
        if self.supports_ansi():
            sys.stdout.write(f'\033[{row};{col}H')
            sys.stdout.flush()
        
    def clamp(self, x, lo, hi):
        return max(lo, min(hi, x))
        
    def render_frame(self, phase=0.0):
        """Render a small planet frame"""
        w = self.radius * 2 + 1
        h = self.radius
        
        shade = " .:-=+*#%@"
        tex = ".,'`^:;_-+=*#%@"
        
        lines = []
        
        # Light direction
        lx, ly, lz = (-0.6, -0.4, 1.0)
        ll = math.sqrt(lx * lx + ly * ly + lz * lz)
        lx, ly, lz = (lx / ll, ly / ll, lz / ll)
        
        for y in range(-h, h + 1):
            row = []
            for x in range(-w, w + 1):
                nx = x / w
                ny = y / h
                d2 = nx * nx + ny * ny
                if d2 > 1.0:
                    row.append(" ")
                    continue
                    
                z = math.sqrt(1.0 - d2)
                
                # Normal and shading
                diff = self.clamp(nx * lx + ny * ly + z * lz, 0.0, 1.0)
                si = int(diff * (len(shade) - 1))
                base = shade[si]
                
                # Longitude/latitude with rotation
                lon = math.atan2(nx, z)
                lat = math.asin(self.clamp(ny, -1.0, 1.0))
                lon2 = lon + phase
                
                # Procedural texture
                c = (
                    math.sin(3.0 * lon2) +
                    0.7 * math.sin(2.0 * lat + 0.8) +
                    0.6 * math.cos(4.0 * lon2 - 1.2) +
                    0.4 * math.sin(5.0 * lon2 + 3.0 * lat)
                )
                
                land = c > 0.9
                
                if land:
                    t = self.clamp((c + 2.5) / 5.0, 0.0, 1.0)
                    ti = int(t * (len(tex) - 1))
                    ch = tex[ti]
                    if diff > 0.75 and ch in ".,'`":
                        ch = "*"
                else:
                    ch = base
                    
                # Rim darkening
                rim = self.clamp((z - 0.08) / 0.92, 0.0, 1.0)
                if rim < 0.25:
                    ch = "."
                    
                row.append(ch)
            lines.append("".join(row).rstrip())
        return lines
        
    def render_single_line(self, phase=0.0):
        """Render a single line representation of the planet"""
        frame = self.render_frame(phase)
        if frame:
            # Find the middle line with most content
            mid_idx = len(frame) // 2
            return frame[mid_idx] if mid_idx < len(frame) else ""
        return ""
        
    def animate_continuously(self, stop_flag, fps=20):
        """Background animation loop for continuous planet spinning"""
        frame_delay = 1.0 / fps
        start_time = time.time()
        
        try:
            self.hide_cursor()
            
            while not stop_flag.is_set():
                current_time = time.time()
                phase = (current_time - start_time) * 1.6  # Same speed as standalone
                
                # Render new frame
                planet_frame = self.render_frame(phase)
                
                if planet_frame and self.supports_ansi():
                    # Position planet starting at row 3 (after top border)
                    for i, line in enumerate(planet_frame):
                        row = 3 + i  # Start from row 3
                        padding = (50 - len(line)) // 2
                        display_line = " " * max(0, padding) + line
                        
                        # Move cursor and update line
                        self.move_cursor_to(row, 1)
                        sys.stdout.write('\033[K')  # Clear line
                        sys.stdout.write(display_line)
                    
                    # Add ATLAS title below the planet (but don't overwrite menu)
                    title_row = 3 + len(planet_frame)
                    title_line = "A T L A S"
                    padding = (50 - len(title_line)) // 2
                    title_display = " " * max(0, padding) + title_line
                    self.move_cursor_to(title_row, 1)
                    sys.stdout.write('\033[K')
                    sys.stdout.write(title_display)
                    
                    # Only update status line if service is running (at specific row, don't interfere with menu)
                    if service_running:
                        status_row = title_row + 2  # Two rows below title
                        planet_line = self.render_single_line(phase)
                        status_line = f"{planet_line}  {strings.MENU_SERVICE_RUNNING}"
                        self.move_cursor_to(status_row, 1)
                        sys.stdout.write('\033[K')
                        sys.stdout.write(status_line)
                    
                    sys.stdout.flush()
                
                time.sleep(frame_delay)
                
        except Exception:
            pass  # Graceful degradation
        finally:
            self.show_cursor()
        
planet_renderer = PlanetRenderer(radius=6)


def start_planet_animation():
    """Start background planet animation"""
    global planet_animation_active, planet_thread, planet_stop_flag
    
    if not planet_renderer.supports_ansi() or planet_animation_active:
        return
        
    planet_stop_flag.clear()
    planet_animation_active = True
    planet_thread = threading.Thread(
        target=planet_renderer.animate_continuously,
        args=(planet_stop_flag, 20),  # 20 FPS like standalone
        daemon=True
    )
    planet_thread.start()

def stop_planet_animation():
    """Stop background planet animation"""
    global planet_animation_active, planet_thread, planet_stop_flag
    
    if planet_animation_active and planet_thread:
        planet_stop_flag.set()
        planet_thread.join(timeout=1.0)
        planet_animation_active = False
        planet_renderer.show_cursor()

def show_menu_with_planet():
    """Display menu with animated planet header"""
    global service_running
    
    # Get current time for initial animation
    current_time = time.time()
    planet_phase = current_time * 1.2  # Animation speed
    
    # Render initial planet frame
    planet_frame = planet_renderer.render_frame(planet_phase)
    
    # Display planet with ATLAS title
    if planet_frame:
        # Center planet only
        for i, line in enumerate(planet_frame):
            padding = (50 - len(line)) // 2
            print(" " * max(0, padding) + line)
        
        # Add ATLAS title below planet
        title_line = "A T L A S"
        padding = (50 - len(title_line)) // 2
        print(" " * max(0, padding) + title_line)
    else:
        # Fallback if planet rendering fails
        print(f"           {strings.MENU_HEADER}")
    
    print("")
    
    # Status with small planet if running
    if service_running:
        planet_line = planet_renderer.render_single_line(planet_phase)
        status_line = f"{planet_line}  {strings.MENU_SERVICE_RUNNING}"
        print(status_line)
    else:
        print(strings.MENU_SERVICE_STOPPED)

def show_menu(debug_mode=False):
    """Display the main menu options with spinning planet"""
    global service_running
    
    # Stop any existing animation to prevent interference
    stop_planet_animation()
    
    # Show static planet header (no background animation)
    show_menu_with_planet()
    
    # Menu options (same for both modes)
    if service_running:
        print(f"1. {strings.MENU_STOP_SERVICE}")
        print(f"2. {strings.MENU_VIEW_LOGS}")
        print(f"3. {strings.MENU_EXIT}")
        if debug_mode:
            print(f"4. {strings.MENU_CLEAR_FILES}")
    else:
        print(f"1. {strings.MENU_START_SERVICE}")
        print(f"2. {strings.MENU_EXIT}")
        if debug_mode:
            print(f"3. {strings.MENU_VIEW_LOGS}")
            print(f"4. {strings.MENU_CLEAR_FILES}")
    
    print("="*50)

def get_user_choice(debug_mode=False):
    """Get and validate user menu choice"""
    global service_running
    
    if service_running:
        max_option = 4 if debug_mode else 3
    else:
        max_option = 4 if debug_mode else 2
    
    while True:
        try:
            choice = input(strings.SELECT_OPTION.format(max_option)).strip()
            
            # Stop planet animation when user provides input
            stop_planet_animation()
            
            if choice.isdigit() and 1 <= int(choice) <= max_option:
                return int(choice)
            else:
                print(strings.INVALID_CHOICE.format(max_option))
        except (KeyboardInterrupt, EOFError):
            # Stop animation before exit
            stop_planet_animation()
            print(f"\n{strings.EXITING}")
            return None


def view_live_logs():
    """View live logs with tail -f, allow return to menu"""
    paths = get_config_paths()
    log_file = paths['log_path']
    
    if not os.path.exists(log_file):
        print(f"\n{strings.LOG_FILE_NOT_FOUND.format(log_file)}")
        print(strings.RUN_SERVICE_FOR_LOGS)
        input(strings.PRESS_ENTER_CONTINUE)
        return
    
    print(f"\n{strings.VIEWING_LIVE_LOGS.format(log_file)}")
    print(f"{strings.PRESS_CTRL_C_RETURN}\n")
    
    try:
        # Use subprocess to run tail -f
        process = subprocess.Popen(
            ['tail', '-f', log_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read and display output until interrupted
        while True:
            output = process.stdout.readline()
            if output:
                print(output.rstrip())
            elif process.poll() is not None:
                break
                
    except KeyboardInterrupt:
        print(f"\n\n{strings.RETURNING_TO_MENU}")
        if process:
            process.terminate()
            process.wait()
    except FileNotFoundError:
        print(strings.TAIL_NOT_FOUND)
        # Fallback for systems without tail command
        try:
            with open(log_file, 'r') as f:
                # Go to end and read backward
                f.seek(0, 2)  # Go to end
                file_size = f.tell()
                f.seek(max(0, file_size - 1000))  # Read last 1000 chars
                content = f.read()
                print(content)
                input(strings.PRESS_ENTER_CONTINUE)
        except Exception as e:
            print(strings.ERROR_READING_LOG.format(e))
            input(strings.PRESS_ENTER_CONTINUE)


def clear_debug_files():
    """Clear database and log files"""
    paths = get_config_paths()
    files_to_remove = [paths['db_path'], paths['log_path']]
    
    print(f"\n{strings.CLEARING_DEBUG_FILES}")
    removed_count = 0
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(strings.REMOVED_FILE.format(os.path.basename(file_path)))
                removed_count += 1
            except Exception as e:
                print(strings.FAILED_TO_REMOVE.format(os.path.basename(file_path), e))
        else:
            print(strings.FILE_NOT_FOUND.format(os.path.basename(file_path)))
    
    print(f"\n{strings.CLEARED_FILES_COUNT.format(removed_count)}")
    input(strings.PRESS_ENTER_CONTINUE)


def start_service_background(db_path, log_path, debug_mode=False):
    """Start the AtlasPi service in a background thread"""
    global service_running, stop_service_flag
    
    def service_wrapper():
        global service_running
        try:
            service_running = True
            logging.info(strings.APP_STARTING)
            run_application_loop(db_path, log_path, debug_mode, stop_service_flag)
        except Exception as e:
            logging.error(f"Service error: {e}")
        finally:
            service_running = False
    
    stop_service_flag.clear()
    thread = threading.Thread(target=service_wrapper, daemon=True)
    thread.start()
    return thread


def stop_service_background():
    """Stop the background AtlasPi service"""
    global service_thread, service_running, stop_service_flag
    
    if service_running and service_thread:
        print(f"\n{strings.STOPPING_SERVICE}")
        stop_service_flag.set()
        service_thread.join(timeout=5)
        service_running = False
        print(strings.SERVICE_STOPPED)
        time.sleep(1)
    else:
        print(strings.SERVICE_NOT_RUNNING)


def run_interactive_menu(debug_mode=False):
    """Run the interactive menu system"""
    global service_thread, service_running
    
    # Initialize paths and config here since we're not exiting to setup.py
    paths = get_config_paths()
    config = load_config(paths['config_path'])
    
    try:
        while True:
            show_menu(debug_mode)
            choice = get_user_choice(debug_mode)
            
            if choice is None:  # User pressed Ctrl+C
                break
                
            # Handle menu choices based on service state
            if not service_running:
                # Service is stopped
                if choice == 1:  # Start service
                    print(f"\n{strings.STARTING_SERVICE_BG}")
                    initialize_database(paths['db_path'], config)
                    service_thread = start_service_background(paths['db_path'], paths['log_path'], debug_mode)
                    time.sleep(1)  # Give service time to start
                    print(strings.SERVICE_STARTED)
                    
                elif choice == 2:  # Exit
                    break
                    
                elif choice == 3 and debug_mode:  # View logs
                    view_live_logs()
                    
                elif choice == 4 and debug_mode:  # Clear files
                    clear_debug_files()
                    
            else:
                # Service is running
                if choice == 1:  # Stop service
                    stop_service_background()
                    
                elif choice == 2:  # View logs
                    view_live_logs()
                    
                elif choice == 3:  # Exit
                    stop_service_background()
                    break
                    
                elif choice == 4 and debug_mode:  # Clear files (stop service first)
                    stop_service_background()
                    clear_debug_files()
                    
    except KeyboardInterrupt:
        print(f"\n{strings.SHUTTING_DOWN}")
        stop_planet_animation()  # Stop planet animation on exit
        if service_running:
            stop_service_background()
    
    # Clean up animation on normal exit
    stop_planet_animation()
    return False  # Always return False since we handle everything internally now