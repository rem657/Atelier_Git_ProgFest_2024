import git
import datetime
import time
import os
import tqdm


def autocommit_once(filepath: str = os.path.join(os.path.dirname(__file__), "autocommit_time.txt")):
    now = datetime.datetime.now()
    with open(filepath, 'w') as f:
        f.write(str(now))

    repo = git.Repo(search_parent_directories=True)
    repo.git.add(filepath)
    repo.git.commit('-m', 'Autocommit')
    repo.git.push()
    return now


def autocommit(
        filepath: str = os.path.join(os.path.dirname(__file__), "autocommit_time.txt"),
        refresh_times_seconds: float = 60.0,
        timeout_seconds: float = 60*60*1.0,
):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    start_time = time.time()
    pbar = tqdm.tqdm(total=timeout_seconds, desc="Autocommitting", unit="s")
    while time.time() - start_time < timeout_seconds:
        now = autocommit_once(filepath)
        pbar.set_postfix_str(f"Last commit: {now}")
        time.sleep(refresh_times_seconds)
        pbar.update(refresh_times_seconds)
    pbar.close()


if __name__ == "__main__":
    autocommit()
