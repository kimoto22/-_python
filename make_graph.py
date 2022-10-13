import matplotlib.pyplot as plt
import pandas as pd
import glob


person = "tanaka"
brain_log_dir = f".\\log_dir\\brain_log\\{person}\\*"
task_log_dir = f".\\log_dir\\task_log\\{person}\\*"

brain_log = glob.glob(brain_log_dir)
task_log = glob.glob(task_log_dir)

for blog_path, tlog_path in zip(brain_log, task_log):
    print(blog_path, tlog_path)
    blog = pd.read_csv(blog_path, encoding = "shift-jis")
    tlog = pd.read_csv(tlog_path, encoding = "shift-jis")

