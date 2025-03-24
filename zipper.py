#!/usr/bin/env python3


import os
import sys
import zipfile
import datetime
import argparse
import time
from pathlib import Path
from typing import List, Set

class FancyPrinter:
    # ANSI escape codes
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'
    
    @classmethod
    def print_banner(cls):
        """Display animated banner"""
        banner = f"""
{cls.CYAN}{cls.BOLD}
╔════════════════════════════════════════════════════════════╗
║ {cls.YELLOW}Zipper made by Bencewok{cls.CYAN}                                    ║
╚════════════════════════════════════════════════════════════╝
{cls.ENDC}"""
        print(banner)

    @classmethod
    def progress_bar(cls, current, total, bar_length=40):
        """Create text-based progress bar"""
        fraction = current / total
        arrow = int(fraction * bar_length - 1) * '─' + '▶'
        padding = (bar_length - len(arrow)) * '─'
        return f"{cls.GREEN}{arrow}{padding}{cls.ENDC} {fraction:.0%}"

    @classmethod
    def spinning_cursor(cls):
        """Generate spinning cursor characters"""
        while True:
            for cursor in '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏':
                yield f"{cls.CYAN}{cursor}{cls.ENDC}"


    @classmethod
    def print_stats(cls, stats):
        """Display statistics in clean, borderless aligned columns"""
        # Calculate maximum lengths considering ANSI codes
        clean_stats = {k: len(k) for k in stats.keys()}
        max_key_len = max(clean_stats.values())
        max_value_len = max(len(str(v)) for v in stats.values())
        
        # Calculate column widths
        key_column_width = max_key_len + 2  # +1 for colon, +1 for padding
        value_column_width = max_value_len + 2  # +1 for padding
        
        # Print header
        print(f"\n{cls.BOLD}📊 Compression Statistics{cls.ENDC}")
        print(f"{cls.CYAN}{'─' * (key_column_width + value_column_width + 1)}{cls.ENDC}")
        
        for key, value in stats.items():
            # Format key and value with proper padding
            key_part = f"{cls.YELLOW}{key}:{cls.ENDC}"
            value_part = f"{cls.GREEN}{value}{cls.ENDC}"
            
            # Calculate padding
            key_padding = key_column_width - (len(key) + 1)  # +1 for colon
            value_padding = value_column_width - len(str(value))
            
            # Create aligned line
            line = (
                f"{' ' * key_padding}"
                f"{key_part}"
                f"{' ' * value_padding}"
                f"{value_part}"
            )
            print(line)

        # Print footer separator
        print(f"{cls.CYAN}{'─' * (key_column_width + value_column_width + 1)}{cls.ENDC}")

def get_excluded_patterns() -> Set[str]:
    """Default exclusion patterns"""
    return {
        '.git', '.github', 'node_modules', '.DS_Store', '__MACOSX',
        '.gitignore', '.env', '.vscode', '.idea', '.zip', 'Thumbs.db',
        'desktop.ini', 'package-lock.json', 'yarn.lock'
    }

def human_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024 or unit == 'GB':
            return f"{size_bytes:.2f} {unit}" if unit != 'B' else f"{size_bytes} B"
        size_bytes /= 1024

def create_zip(source_dir: str, output_path: str, custom_name: str = None, exclude: List[str] = None, use_timestamp: bool = True):
    """Main zipping function with visual feedback"""
    start_time = time.time()
    exclude_patterns = get_excluded_patterns().union(set(exclude or []))
    spinner = FancyPrinter.spinning_cursor()
    
    # File discovery phase
    file_paths = []
    total_size = 0
    print(f"{FancyPrinter.BLUE}🔍 Discovering files...{FancyPrinter.ENDC}")
    
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if d not in exclude_patterns]
        for file in files:
            if file not in exclude_patterns:
                path = Path(root) / file
                file_paths.append(path)
                total_size += path.stat().st_size
                sys.stdout.write(f"\r{next(spinner)} Found {len(file_paths)} files")
                sys.stdout.flush()
    
    if not file_paths:
        print(f"\n{FancyPrinter.RED}❌ No files found to zip!{FancyPrinter.ENDC}")
        sys.exit(1)
    
    # Zip creation phase
    base_name = custom_name or Path(source_dir).name
    
    # Apply timestamp only if use_timestamp is True
    if use_timestamp:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"{base_name}_{timestamp}.zip"
    else:
        zip_filename = f"{base_name}.zip"
        
    zip_path = Path(output_path) / zip_filename
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"\n{FancyPrinter.BLUE}🚀 Starting compression...{FancyPrinter.ENDC}")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, file_path in enumerate(file_paths, 1):
                rel_path = file_path.relative_to(source_dir)
                zipf.write(file_path, rel_path)
                
                # Update progress
                progress = FancyPrinter.progress_bar(i, len(file_paths))
                sys.stdout.write(f"\r{progress} {FancyPrinter.CYAN}Compressing: {rel_path}{' ' * 10}")
                sys.stdout.flush()
        
        # Calculate statistics
        zip_size = zip_path.stat().st_size
        stats = {
            "Source Directory": Path(source_dir).name,
            "Total Files": str(len(file_paths)),
            "Original Size": human_size(total_size),
            "Compressed Size": human_size(zip_size),
            "Compression Ratio": f"{(1 - zip_size/total_size)*100:.1f}%",
            "Processing Time": f"{time.time() - start_time:.2f}s"
        }
        
        print(f"\n{FancyPrinter.GREEN}✅ Successfully created archive:{FancyPrinter.ENDC}")
        print(f"{FancyPrinter.CYAN}📦 {zip_path.resolve()}{FancyPrinter.ENDC}")
        FancyPrinter.print_stats(stats)
        
    except Exception as e:
        print(f"\n{FancyPrinter.RED}❌ Error: {e}{FancyPrinter.ENDC}")
        sys.exit(1)

def main():
    FancyPrinter.print_banner()
    
    parser = argparse.ArgumentParser(
        description="Advanced directory zipper with rich visual feedback",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-s", "--source",
        help="Directory to compress",
        default=os.getcwd())
    parser.add_argument("-o", "--output",
        help="Output directory",
        default=os.getcwd())
    parser.add_argument("-n", "--name",
        help="Custom base name for archive")
    parser.add_argument("-e", "--exclude",
        help="Comma-separated patterns to exclude",
        default="")
    parser.add_argument("--no-timestamp", 
        action="store_true",
        help="Exclude timestamp from filename")
    
    args = parser.parse_args()
    
    create_zip(
        source_dir=args.source,
        output_path=args.output,
        custom_name=args.name,
        exclude=args.exclude.split(',') if args.exclude else [],
        use_timestamp=not args.no_timestamp
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{FancyPrinter.YELLOW}🛑 Operation cancelled by user{FancyPrinter.ENDC}")
        sys.exit(0)