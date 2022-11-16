Title: A Quick Guide to on How to Safely Store and Retrieve Sensitive Data
Date: 2022-11-15
Modified: 2022-11-15
Status: published
Tags: analytics, datascience, databases, sql
Slug: envvar
Authors: Brian Roepke
Summary: Never put user names, passwords, or API keys in your code.  Leverage environment varialble to keep your data safe.
Description: Learn how to leverage environment variables and the OS library in Python to keep sensitive data safe.  A few small tweaks to your habits will keep you safe.
Header_Cover: images/covers/safe.jpg
Og_Image: images/covers/safe.jpg
Twitter_Image: images/covers/safe.jpg

# Working with Environment Variables in Python

**Note:** *This article advises a safe way to store and retrieve sensitive data from Environment Variables when developing locally. When working in corporate environments, follow recommended best practices from your company.*

If you've ever worked with any API (such as Twitter) or tried to connect to any remote data source, you've probably come across the need to pass in sensitive parameters such as **API Keys**, **User Names**, and **Passwords**. Do you use GitHub to showcase your work? If you do, and you've entered these values as plain text in your notebooks or code, surely you've gotten the email warning that your sensitive information is public! 

```python
twitter_api_key = 'frBtFyG7JefJcBRHY7A6SnTlyOuT2iPAUg4567ndbhKpj9vERw'
```

The good news is that you can get into a simple habit that will keep your keys, secrets, and sensitive information private only to you. We'll leverage **Environment Variables** and a simple Python library called `os` that will allow us to retrieve these values from our local machine.

## What are Environment Variables?

**Environment Variables** are stored in your user profile locally on your machine. They can be ready dynamically in python when executing your code and keep sensitive data out of human-readable code.

## Adding Environment Variables

Let's get started by adding our environment variables. The **.zshrc** is a configuration file that contains the commands that run the zsh shell, just like the **.bashrc** file that contains commands for the bash shell. You can run the following command to see your **.zshrc** file. Note that it's a hidden file, so you must add the `-a` parameter to the `ls` command.

```bash
ls -a
```

## Time for a Light Intro to VIM

Now we're going to get into a little **VIM**. VIM is an open-source screen-based text editor that's built-in MacOS. VIM can be *a bit* complicated to get used to if you've never been exposed to it, but it's quite powerful. If you're unfamiliar with VIM, I recommend you check out this [VIM Tutorial](https://www.openvim.com/). I'll run through the exact basic command you'll need to add your environment variables to the **.zshrc** file. Let's start by opening our **.zshrc** file in VIM.

```bash
vim .zshrc
```

Your **.zshrc** file will open with various settings depending on what other solutions have been written to it. It might look something like this where I have Anaconda installed already.

```bash
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/brianroepke/miniforge3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/brianroepke/miniforge3/etc/profile.d/conda.sh" ]; then
        . "/Users/brianroepke/miniforge3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/brianroepke/miniforge3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

Next, we can navigate around. There are two modes in VIM. The editor will open in **normal** mode, where you can navigate around the file. Your trackpad/mouse should be fine, or you can use arrow keys. Scroll to the bottom of your file and press `i` to enter **insert** mode. Now you can add your environment variables. I'll add a couple of examples below.

```bash
export USER="test_user"
export PW="some_very_hard_to_crack_password"
export HOST="foo.bar.net"
```

Press `esc` to exit **insert** mode. Now you can navigate around the file. Press `:` to enter **command** mode. Type `wq` and press `enter` to save and quit.

When you add to the **.zshrc** file or make changes, you need to reload the file to make the changes effective. Run the following command in the zsh shell to reload the configuration file and make your changes effective.

**Note:** I sometimes find that even after I do this, I need to reboot my computer to get python to be able to read them with the `os.environ` command.

```bash
source ~/.zshrc 
```

Check your new **environment variables** with the following command:

```bash
export
```

Repeat this process whenever you get a new set of sensitive information you need to use in a project. One thing that works well for me is using descriptive names for them, such as `TWITTER_API_KEY` or `TWITTER_API_SECRET`. This way, you can easily remember what they are for and add them to your **.zshrc** file.

## Using Environment Variables in Python

The Rest is easy! Now we can use our environment variables in **Python**. Let's start by importing the `os` library.

```python
import os
```

Then we use the `os.environ` command to get the value of our environment variable and store them in memory.

```python
USER = os.environ.get("USER")
PW = os.environ.get("PASS")
HOST = os.environ.get("HOST")
```

Like any other variable, you can pass them into functions, connection strings, or whatever you'd like. Here's an example of how you might use them in a connection string.

```python
uri = f"mongodb+srv://{USER}:{PW}@{HOST}"
client = MongoClient(uri)
```

Check out my [article]({filename}mongo.md) on pulling data from MongoDB with Python for more details on how to use this connection string.


## Conclusion

Knowing how to store and retrieve sensitive data properly is critical for any data scientist and analyst. It's a really simple habit to get into that will ensure you're not exposing sensitive information to the world or possibly looking silly in your first professional role! We started by adding our environment variables to the **.zshrc** file. Then we used the `os` library to retrieve them in Python. Now you're ready to go!

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Safe Photo by <a href="https://unsplash.com/@moneyphotos?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">regularguy.eth</a> on <a href="https://unsplash.com/s/photos/safe?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  