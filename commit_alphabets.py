import datetime
import os
from datetime import date
from pathlib import Path
from typing import List, Tuple

import numpy as np
from fire import Fire
from git import Repo, Actor

from alphabet_matrix import word_matrix, week_count_for_group


def create_repo(repo_dir):
    # type: (Path) -> Repo
    if not repo_dir.exists():
        repo_dir.mkdir(exist_ok=True)
    os.chdir(str(repo_dir))
    repo = Repo.init(str(repo_dir))
    print('Create new repo under {}'.format(repo_dir))
    return repo


def create_commit(repo, commit_filename, name, email, commit_date):
    # type: (Repo, str, str, str, date) -> None
    # commit_file = Path(repo.working_dir) / commit_filename
    with open(commit_filename, 'a') as fw:
        fw.write('dd')
        fw.close()

    action_date = commit_date.strftime("%Y-%m-%dT%H:%M:%S")
    os.environ["GIT_AUTHOR_DATE"] = action_date
    os.environ["GIT_COMMITTER_DATE"] = action_date
    repo.git.add(commit_filename)
    actor = Actor(name, email=email)
    repo.index.commit("commit", author=actor)


def week_for_group(word_group):
    # type: (List[str]) -> int
    no_of_weeks = week_count_for_group(word_group)
    return 26 - no_of_weeks // 2


def group_by_size(words, max_per_group=50):
    # type: (List[str], int) -> List[List[str]]
    groups = []  # type: List[List[str]]
    current_group = []  # type: List[str]
    for word in words:
        group_size = week_count_for_group(current_group + [word])
        if group_size > max_per_group:
            groups.append(current_group)
            current_group = [word]
        else:
            current_group.append(word)

    if len(current_group) > 0:
        groups.append(current_group)

    return groups


def date_from_week_number(year, week_number):
    date_str = '{}-W{}-0'.format(year, week_number)
    return datetime.datetime.strptime(date_str, "%Y-W%W-%w")


def create_named_commits(repo_dir, words, start_year, name, email, commit_range=(6, 10)):
    # type: (Path, List[str], int, str, str, Tuple[int, int]) -> None
    repo = create_repo(Path(repo_dir))
    groups = group_by_size(words)
    print(groups)
    for i, group in enumerate(groups):
        print('Group: {}, {}'.format(i, group))
        current_year = start_year + i
        sentence = ' '.join(group)
        word_mat = word_matrix(sentence)
        week_number = week_for_group(group)
        current_date = date_from_week_number(current_year, week_number) + datetime.timedelta(hours=10)
        print('Sentence: {}, week: {}, start date: {}, word mat shape: {}'.format(sentence, week_number,
                                                                                  current_date, word_mat.shape))
        for i in range(word_mat.shape[1]):
            for j in range(word_mat.shape[0]):
                if word_mat[j, i] == 1:
                    no_of_commits = np.random.randint(commit_range[0], commit_range[1])
                    for _ in range(no_of_commits):
                        create_commit(repo, 'hello_world', name, email, current_date)
                current_date += datetime.timedelta(days=1)


"""
1) Create a test repo with words you want to write in dummy repository.
    python3 -m commit_alphabets \
        --repo_dir /tmp/test_repo \
        --words LIFE,AND,UNIVERSE \
        --start_year 1991 \
        --name "Billi" \
        --email abc@gmail.com
2) Push the newly created repository to github.    
"""
if __name__ == '__main__':
    Fire(create_named_commits)
