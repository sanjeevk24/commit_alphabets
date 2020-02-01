# commit_alphabets
A python script for writing messages on GitHub's contribution dashboard.

## Example
- Create a test repo with words you want to write in dummy repository.
    ```
    python3 -m commit_alphabets \
        --repo_dir /tmp/test_repo \
        --words LIFE,AND,UNIVERSE \
        --start_year 1991 \
        --name "Billi" \
        --email abc@gmail.com
- Push the newly created repository to github.    
