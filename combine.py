import os
import pandas as pd

# Path to the folder containing CSV files
csv_folder = './'
annotation_file = 'annotation.csv'

# List all CSV files in the folder
csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

# Sort CSV files numerically based on the sequence number at the start of the filename
csv_files.sort(key=lambda x: int(x.split('_')[0]))

# Define activity labels for each segment
activity_labels = [0] * 24 + [1] * 24 + [2] * 24

# Ensure the number of files matches the number of labels
if len(csv_files) != len(activity_labels):
    print("Error: The number of CSV files does not match the number of activity labels.")
else:
    # Create the annotation data
    annotation_data = {
        'filename': csv_files,
        'activity': activity_labels
    }

    # Create a DataFrame and save it as a CSV
    annotation_df = pd.DataFrame(annotation_data)
    annotation_df.to_csv(annotation_file, index=False)
    print(f"Annotation file '{annotation_file}' created successfully.")
