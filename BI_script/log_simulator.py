# This script continuously reads impression_log.csv and routes each line into the corresponding date folder under log_stream.
# Usage: python stream_logs.py --csv path/to/impression_log.csv --base-dir path/to/log_stream

import argparse
import csv
import os
import time
import pandas as pd
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

def process_batch(batch, base_dir):
    """Process a batch of data and write it to a file"""
    # Convert dates and create date columns
    batch['date'] = pd.to_datetime(batch['start_time']).dt.date
    
    # Group by date
    grouped = batch.groupby('date')
    
    # Process data for each date
    for date, group in grouped:
        date_str = date.strftime('%Y-%m-%d')
        folder_path = os.path.join(base_dir, date_str)
        
        # Ensure that the directory exists
        os.makedirs(folder_path, exist_ok=True)
        
        out_file = os.path.join(folder_path, 'impression_log.csv')
        
        # Write in append mode, and if it is a new file, write the header
        write_header = not os.path.exists(out_file)
        
        # Use a faster to_csv method
        group[['user_id', 'news_id', 'start_time', 'duration']].to_csv(
            out_file,
            mode='a',
            header=write_header,
            index=False,
            quoting=csv.QUOTE_NONNUMERIC
        )

def main():
    parser = argparse.ArgumentParser(description="Stream impression_log by date into per-day folders.")
    parser.add_argument('--csv', required=True, help='Path to impression_log.csv')
    parser.add_argument('--base-dir', required=True, help='Base directory for log_stream/YYYY-MM-DD folders')
    parser.add_argument('--batch-size', type=int, default=100000, help='Number of rows per batch (default: 100,000)')
    parser.add_argument('--workers', type=int, default=0, help='Number of parallel workers (0 = auto-detect)')
    args = parser.parse_args()

    # Ensuring base directory exists
    print(f"Ensuring base directory exists: {args.base_dir}")
    os.makedirs(args.base_dir, exist_ok=True)
    
    # count workers
    if args.workers == 0:
        args.workers = max(1, multiprocessing.cpu_count() - 1)
    
    print(f"Processing {args.csv} with batch size {args.batch_size} and {args.workers} workers")
    
    # Retrieve the total file size for progress tracking
    total_size = os.path.getsize(args.csv)
    processed_size = 0
    processed_rows = 0
    start_time = time.time()
    
    # Using block reading to process large files
    for batch in pd.read_csv(
        args.csv,
        chunksize=args.batch_size,
        dtype={
            'user_id': 'string',
            'news_id': 'string',
            'start_time': 'string',
            'duration': 'int32'
        },
        engine='c'  # Use a faster C engine
    ):
        # Parallel processing using thread pool
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(process_batch, batch.copy(), args.base_dir)]
            
            # Waiting for all tasks to be completed
            for future in as_completed(futures):
                # You can handle exceptions here
                pass
        
        # Progress
        processed_rows += len(batch)
        processed_size += args.batch_size * 100  # 近似值，实际更准确
        
        # Regularly print progress
        if processed_rows % (10 * args.batch_size) == 0:
            elapsed = time.time() - start_time
            rows_per_sec = processed_rows / elapsed
            mb_per_sec = processed_size / (1024 * 1024) / elapsed
            
            print(
                f"Processed {processed_rows:,} rows | "
                f"{rows_per_sec:,.0f} rows/sec | "
                f"{mb_per_sec:.2f} MB/sec | "
                f"Elapsed: {elapsed:.1f}s"
            )
    
    total_time = time.time() - start_time
    print(f"Completed processing {processed_rows:,} rows in {total_time:.1f} seconds")
    print(f"Average speed: {processed_rows/total_time:,.0f} rows/sec")

if __name__ == "__main__":
    main()