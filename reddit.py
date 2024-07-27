{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Loading And Fetching Data From Reddit PRAW"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "SECRET_KEY = 'LyyFU_r17F6s1i0ajYI2dxoSi2dOtw'\n",
    "CLIENT_ID = 'SMi4R1E-3TeMoXqqwPNwUg'\n",
    "USER_NAME = 'Weary-Tooth7440'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: praw in c:\\python311\\lib\\site-packages (7.7.1)\n",
      "Requirement already satisfied: prawcore<3,>=2.1 in c:\\python311\\lib\\site-packages (from praw) (2.4.0)\n",
      "Requirement already satisfied: update-checker>=0.18 in c:\\python311\\lib\\site-packages (from praw) (0.18.0)\n",
      "Requirement already satisfied: websocket-client>=0.54.0 in c:\\users\\jamie\\appdata\\roaming\\python\\python311\\site-packages (from praw) (1.5.1)\n",
      "Requirement already satisfied: requests<3.0,>=2.6.0 in c:\\python311\\lib\\site-packages (from prawcore<3,>=2.1->praw) (2.28.1)\n",
      "Requirement already satisfied: charset-normalizer<3,>=2 in c:\\python311\\lib\\site-packages (from requests<3.0,>=2.6.0->prawcore<3,>=2.1->praw) (2.1.1)\n",
      "Requirement already satisfied: idna<4,>=2.5 in c:\\python311\\lib\\site-packages (from requests<3.0,>=2.6.0->prawcore<3,>=2.1->praw) (3.4)\n",
      "Requirement already satisfied: urllib3<1.27,>=1.21.1 in c:\\python311\\lib\\site-packages (from requests<3.0,>=2.6.0->prawcore<3,>=2.1->praw) (1.26.13)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in c:\\python311\\lib\\site-packages (from requests<3.0,>=2.6.0->prawcore<3,>=2.1->praw) (2022.12.7)\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "[notice] A new release of pip is available: 23.1.2 -> 24.1.2\n",
      "[notice] To update, run: python.exe -m pip install --upgrade pip\n"
     ]
    }
   ],
   "source": [
    "%pip install praw"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import math\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "sns.set(style='darkgrid', context='talk', palette='Dark2')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "import praw\n",
    "\n",
    "# Initialize Reddit instance\n",
    "reddit = praw.Reddit(client_id=CLIENT_ID,\n",
    "                     client_secret=SECRET_KEY,\n",
    "                     user_agent=USER_NAME)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Display Name: stocks\n",
      "Title: Stocks - Investing and trading for all\n",
      "Description: Almost any post related to stocks is welcome; please read the rules below:\n",
      "\n",
      "[**If you're new here**](https://www.reddit.com/r/stocks/comments/4x1419/if_youre_new_here_read_this_post_first/)\n",
      "\n",
      "##Resources\n",
      "\n",
      "* [Wiki for new investors](https://www.reddit.com/r/stocks/wiki/index)\n",
      "\n",
      "* [Pattern day trading](https://www.reddit.com/r/stocks/wiki/pdtrules)\n",
      "\n",
      "* [Earnings calendar](https://finance.yahoo.com/calendar/earnings/)\n",
      "\n",
      "##Karma requirements\n",
      "\n",
      "[Click here to find how many days old your account needs to be and how much karma you need](https://www.reddit.com/r/stocks/wiki/karma) before you can comment or post to r/Stocks.\n",
      "\n",
      "##Rules [(in depth rules wiki here)](https://www.reddit.com/r/stocks/wiki/rules)\n",
      "\n",
      "1. Disclose any related open positions when discussing a particular stock or financial instrument.\n",
      "\n",
      "2. Spam, ads, solicitations (including referral links), and self-promotion posts or comments will be removed and you might get banned.  Instead, [advertise here.](https://about.reddit.com/advertise/)\n",
      "\n",
      "3. Context & effort must be provided; empty posts or empty posts with links will be automatically removed.  [Low effort mentions for meme stocks will be removed, see here.](https://www.reddit.com/r/stocks/wiki/meme-stocks)\n",
      "\n",
      "4. The Robinhood app should be discussed in /r/Robinhood. Posts regarding this topic will be automatically removed.\n",
      "\n",
      "5. Trolling, insults, or harassment, especially in posts requesting advice, will be removed.\n",
      "\n",
      "6. No bitcoin or crypto discussions unrelated to stocks.  Non-ETF-related Crypto goes on r/CryptoCurrencies [info. ](https://www.reddit.com/r/stocks/wiki/crypto-general)\n",
      "\n",
      "7. No penny stock discussions, including OTC, microcaps, pump & dumps, low vol pumps and SPACs.  Consider posting to r/SPACs, r/pennystocks, or r/weedstocks instead.  [Read here for more info.](https://www.reddit.com/r/stocks/wiki/pennystocks)\n",
      "\n",
      "8. Almost any post related to stocks and investment is welcome on /r/stocks, including pre IPO news, futures & forex related to stocks, and geopolitical or corporate events indicating risks; outside this is offtopic and can be removed.\n",
      "\n",
      "##Filter By Flair\n",
      "\n",
      "* [News](https://www.reddit.com/r/stocks/search?q=flair%3A%22News%22+-flair%3A%22Ticker+News%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Discussion](https://www.reddit.com/r/stocks/search?q=flair%3A%22Discussion%22+-flair%3A%22Ticker+Discussion%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Question](https://www.reddit.com/r/stocks/search?q=flair%3A%22Question%22+-flair%3A%22Ticker+Question%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Advice Request](https://www.reddit.com/r/stocks/search?q=flair%3A%22Advice%2BRequest%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Advice](https://www.reddit.com/r/stocks/search?q=flair%3A%22Advice%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Ticker News](https://www.reddit.com/r/stocks/search?q=flair%3A%22Ticker%2BNews%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Ticker Discussion](https://www.reddit.com/r/stocks/search?q=flair%3A%22Ticker%2BDiscussion%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Ticker Question](https://www.reddit.com/r/stocks/search?q=flair%3A%22Ticker%2BQuestion%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Trades](https://www.reddit.com/r/stocks/search?q=flair%3A%22Trades%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Resources](https://www.reddit.com/r/stocks/search?q=flair%3A%22Resources%22&restrict_sr=on&sort=new&t=all)\n",
      "* [AMA](https://www.reddit.com/r/stocks/search?q=flair%3A%22AMA%22&restrict_sr=on&sort=new&t=all)\n",
      "* [Off-Topic](https://www.reddit.com/r/stocks/search?q=flair%3A%22Off-Topic%22&restrict_sr=on&sort=new&t=all)\n",
      "\n",
      "##Earnings calendar\n",
      "\n",
      "* [Yahoo earnings calendar](https://finance.yahoo.com/calendar/earnings/)\n",
      "* [Bloomberg earnings calendar](https://markets.businessinsider.com/earnings-calendar)\n",
      "\n",
      "##Related Subreddits (see the rules above for related subs as well)\n",
      "\n",
      "* /r/personalfinance\n",
      "* /r/options\n",
      "* /r/thetagang\n",
      "* /r/investing\n",
      "* /r/Economics\n",
      "* /r/StockMarket\n",
      "* /r/Forex\n",
      "* /r/realestate\n",
      "* /r/wallstreetbets\n",
      "\n",
      "###### [Most information to help you learn and practice can be found in our wiki.](https://www.reddit.com/r/stocks/wiki/index)\n",
      "\n",
      "*logo by u/aDrunkLlama.  [Link to logo](https://i.imgur.com/pH7Ceda.png)\n"
     ]
    }
   ],
   "source": [
    "def get_subreddit_data(subreddit_name):\n",
    "    subreddit = reddit.subreddit(subreddit_name)\n",
    "\n",
    "    return subreddit\n",
    "\n",
    "# Display the name of the Subreddit\n",
    "stocks_subreddit = get_subreddit_data('stocks')\n",
    "wall_street_bets_subreddit = get_subreddit_data('wallstreetbets')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_subreddit_data(subreddit_names):\n",
    "    data = []\n",
    "    for subreddit_name in subreddit_names:\n",
    "        subreddit = reddit.subreddit(subreddit_name)\n",
    "        # ... (rest of your existing code to scrape data)\n",
    "        for post in subreddit.search('daily discussion', sort='new', time_filter='week'):\n",
    "            if post.num_comments > 0:\n",
    "                # Scraping comments for each post\n",
    "                post.comments.replace_more(limit= 5)\n",
    "                for comment in post.comments.list():\n",
    "                    data.append({\n",
    "                        'id': post.id + '_' +  comment.id ,\n",
    "                       'Author': comment.author.name if comment.author else 'Unknown',\n",
    "                        'Timestamp': pd.to_datetime(comment.created_utc, unit='s'),\n",
    "                        'Text': comment.body,\n",
    "                        'Score': comment.score,\n",
    "                        'Post_url':post.url,\n",
    "                    })\n",
    "    return data\n",
    "\n",
    "# Example usage:\n",
    "subreddit_names = ['stocks', 'wallstreetbets']\n",
    "all_data = get_subreddit_data(subreddit_names)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create pandas DataFrame for posts and comments\n",
    "df = pd.DataFrame(all_data)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Cleaning The Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def DropDeletedComment(data):\n",
    "\n",
    "  #Dropping the text with [deleted] and [removed]\n",
    "  data = data[~data['Text'].str.contains('\\[removed\\]|\\[deleted\\]', na=False, regex = True)]\n",
    "  data = data.reset_index(drop=True)\n",
    "\n",
    "  return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def ReplaceParagraphBrake(data):\n",
    "  #Replacing the Paragraph Brake\n",
    "  data['Text'] = data['Text'].str.replace('\\n', ' ')\n",
    "  data = data.reset_index(drop=True)\n",
    "\n",
    "  return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def DropSpamComment(data):\n",
    "\n",
    "  #Dropping the text with spam words\n",
    "    data = data[~data['Text'].str.contains('\\b(free|sale|discount|limited time|offer|buy now|click here)\\b', na=False, regex = True)]\n",
    "    data = data.reset_index(drop=True)\n",
    "\n",
    "    return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def RemoveURL(data):\n",
    "  #Removing the URL\n",
    "  data['Text'] = data['Text'].str.replace(r'http\\S+', '')\n",
    "  data = data.reset_index(drop=True)\n",
    "\n",
    "  return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def RemoveUser(data):\n",
    "  #Removing the User\n",
    "  data['Text'] = data['Text'].str.replace(r'@\\w+', '')\n",
    "  data = data.reset_index(drop=True)\n",
    "\n",
    "  return data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = DropDeletedComment(df)\n",
    "df = ReplaceParagraphBrake(df)\n",
    "df = DropSpamComment(df)\n",
    "df = RemoveURL(df)\n",
    "df = RemoveUser(df)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Preprocessing Comment"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: nltk in c:\\python311\\lib\\site-packages (3.8.1)\n",
      "Requirement already satisfied: click in c:\\python311\\lib\\site-packages (from nltk) (8.1.3)\n",
      "Requirement already satisfied: joblib in c:\\python311\\lib\\site-packages (from nltk) (1.2.0)\n",
      "Requirement already satisfied: regex>=2021.8.3 in c:\\python311\\lib\\site-packages (from nltk) (2024.5.15)\n",
      "Requirement already satisfied: tqdm in c:\\python311\\lib\\site-packages (from nltk) (4.64.1)\n",
      "Requirement already satisfied: colorama in c:\\python311\\lib\\site-packages (from click->nltk) (0.4.6)\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "[notice] A new release of pip is available: 23.1.2 -> 24.1.2\n",
      "[notice] To update, run: python.exe -m pip install --upgrade pip\n"
     ]
    }
   ],
   "source": [
    "%pip install nltk"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "ename": "LookupError",
     "evalue": "\n**********************************************************************\n  Resource \u001b[93mpunkt\u001b[0m not found.\n  Please use the NLTK Downloader to obtain the resource:\n\n  \u001b[31m>>> import nltk\n  >>> nltk.download('punkt')\n  \u001b[0m\n  For more information see: https://www.nltk.org/data.html\n\n  Attempted to load \u001b[93mtokenizers/punkt/english.pickle\u001b[0m\n\n  Searched in:\n    - 'C:\\\\Users\\\\Jamie/nltk_data'\n    - 'c:\\\\Python311\\\\nltk_data'\n    - 'c:\\\\Python311\\\\share\\\\nltk_data'\n    - 'c:\\\\Python311\\\\lib\\\\nltk_data'\n    - 'C:\\\\Users\\\\Jamie\\\\AppData\\\\Roaming\\\\nltk_data'\n    - 'C:\\\\nltk_data'\n    - 'D:\\\\nltk_data'\n    - 'E:\\\\nltk_data'\n    - ''\n**********************************************************************\n",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mLookupError\u001b[0m                               Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[29], line 5\u001b[0m\n\u001b[0;32m      2\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mnltk\u001b[39;00m\n\u001b[0;32m      3\u001b[0m text \u001b[38;5;241m=\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mNLP is amazing! Let\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;124ms explore its wonders.\u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[1;32m----> 5\u001b[0m tokens \u001b[38;5;241m=\u001b[39m \u001b[43mnltk\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mword_tokenize\u001b[49m\u001b[43m(\u001b[49m\u001b[43mtext\u001b[49m\u001b[43m)\u001b[49m\n",
      "File \u001b[1;32mc:\\Python311\\Lib\\site-packages\\nltk\\tokenize\\__init__.py:129\u001b[0m, in \u001b[0;36mword_tokenize\u001b[1;34m(text, language, preserve_line)\u001b[0m\n\u001b[0;32m    114\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mword_tokenize\u001b[39m(text, language\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124menglish\u001b[39m\u001b[38;5;124m\"\u001b[39m, preserve_line\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mFalse\u001b[39;00m):\n\u001b[0;32m    115\u001b[0m \u001b[38;5;250m    \u001b[39m\u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[0;32m    116\u001b[0m \u001b[38;5;124;03m    Return a tokenized copy of *text*,\u001b[39;00m\n\u001b[0;32m    117\u001b[0m \u001b[38;5;124;03m    using NLTK's recommended word tokenizer\u001b[39;00m\n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m    127\u001b[0m \u001b[38;5;124;03m    :type preserve_line: bool\u001b[39;00m\n\u001b[0;32m    128\u001b[0m \u001b[38;5;124;03m    \"\"\"\u001b[39;00m\n\u001b[1;32m--> 129\u001b[0m     sentences \u001b[38;5;241m=\u001b[39m [text] \u001b[38;5;28;01mif\u001b[39;00m preserve_line \u001b[38;5;28;01melse\u001b[39;00m \u001b[43msent_tokenize\u001b[49m\u001b[43m(\u001b[49m\u001b[43mtext\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mlanguage\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m    130\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m [\n\u001b[0;32m    131\u001b[0m         token \u001b[38;5;28;01mfor\u001b[39;00m sent \u001b[38;5;129;01min\u001b[39;00m sentences \u001b[38;5;28;01mfor\u001b[39;00m token \u001b[38;5;129;01min\u001b[39;00m _treebank_word_tokenizer\u001b[38;5;241m.\u001b[39mtokenize(sent)\n\u001b[0;32m    132\u001b[0m     ]\n",
      "File \u001b[1;32mc:\\Python311\\Lib\\site-packages\\nltk\\tokenize\\__init__.py:106\u001b[0m, in \u001b[0;36msent_tokenize\u001b[1;34m(text, language)\u001b[0m\n\u001b[0;32m     96\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21msent_tokenize\u001b[39m(text, language\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124menglish\u001b[39m\u001b[38;5;124m\"\u001b[39m):\n\u001b[0;32m     97\u001b[0m \u001b[38;5;250m    \u001b[39m\u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[0;32m     98\u001b[0m \u001b[38;5;124;03m    Return a sentence-tokenized copy of *text*,\u001b[39;00m\n\u001b[0;32m     99\u001b[0m \u001b[38;5;124;03m    using NLTK's recommended sentence tokenizer\u001b[39;00m\n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m    104\u001b[0m \u001b[38;5;124;03m    :param language: the model name in the Punkt corpus\u001b[39;00m\n\u001b[0;32m    105\u001b[0m \u001b[38;5;124;03m    \"\"\"\u001b[39;00m\n\u001b[1;32m--> 106\u001b[0m     tokenizer \u001b[38;5;241m=\u001b[39m \u001b[43mload\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;124;43mf\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mtokenizers/punkt/\u001b[39;49m\u001b[38;5;132;43;01m{\u001b[39;49;00m\u001b[43mlanguage\u001b[49m\u001b[38;5;132;43;01m}\u001b[39;49;00m\u001b[38;5;124;43m.pickle\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m)\u001b[49m\n\u001b[0;32m    107\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m tokenizer\u001b[38;5;241m.\u001b[39mtokenize(text)\n",
      "File \u001b[1;32mc:\\Python311\\Lib\\site-packages\\nltk\\data.py:750\u001b[0m, in \u001b[0;36mload\u001b[1;34m(resource_url, format, cache, verbose, logic_parser, fstruct_reader, encoding)\u001b[0m\n\u001b[0;32m    747\u001b[0m     \u001b[38;5;28mprint\u001b[39m(\u001b[38;5;124mf\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m<<Loading \u001b[39m\u001b[38;5;132;01m{\u001b[39;00mresource_url\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124m>>\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[0;32m    749\u001b[0m \u001b[38;5;66;03m# Load the resource.\u001b[39;00m\n\u001b[1;32m--> 750\u001b[0m opened_resource \u001b[38;5;241m=\u001b[39m \u001b[43m_open\u001b[49m\u001b[43m(\u001b[49m\u001b[43mresource_url\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m    752\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mformat\u001b[39m \u001b[38;5;241m==\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mraw\u001b[39m\u001b[38;5;124m\"\u001b[39m:\n\u001b[0;32m    753\u001b[0m     resource_val \u001b[38;5;241m=\u001b[39m opened_resource\u001b[38;5;241m.\u001b[39mread()\n",
      "File \u001b[1;32mc:\\Python311\\Lib\\site-packages\\nltk\\data.py:876\u001b[0m, in \u001b[0;36m_open\u001b[1;34m(resource_url)\u001b[0m\n\u001b[0;32m    873\u001b[0m protocol, path_ \u001b[38;5;241m=\u001b[39m split_resource_url(resource_url)\n\u001b[0;32m    875\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m protocol \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m \u001b[38;5;129;01mor\u001b[39;00m protocol\u001b[38;5;241m.\u001b[39mlower() \u001b[38;5;241m==\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mnltk\u001b[39m\u001b[38;5;124m\"\u001b[39m:\n\u001b[1;32m--> 876\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[43mfind\u001b[49m\u001b[43m(\u001b[49m\u001b[43mpath_\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mpath\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m+\u001b[39;49m\u001b[43m \u001b[49m\u001b[43m[\u001b[49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m]\u001b[49m\u001b[43m)\u001b[49m\u001b[38;5;241m.\u001b[39mopen()\n\u001b[0;32m    877\u001b[0m \u001b[38;5;28;01melif\u001b[39;00m protocol\u001b[38;5;241m.\u001b[39mlower() \u001b[38;5;241m==\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mfile\u001b[39m\u001b[38;5;124m\"\u001b[39m:\n\u001b[0;32m    878\u001b[0m     \u001b[38;5;66;03m# urllib might not use mode='rb', so handle this one ourselves:\u001b[39;00m\n\u001b[0;32m    879\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m find(path_, [\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m\"\u001b[39m])\u001b[38;5;241m.\u001b[39mopen()\n",
      "File \u001b[1;32mc:\\Python311\\Lib\\site-packages\\nltk\\data.py:583\u001b[0m, in \u001b[0;36mfind\u001b[1;34m(resource_name, paths)\u001b[0m\n\u001b[0;32m    581\u001b[0m sep \u001b[38;5;241m=\u001b[39m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m*\u001b[39m\u001b[38;5;124m\"\u001b[39m \u001b[38;5;241m*\u001b[39m \u001b[38;5;241m70\u001b[39m\n\u001b[0;32m    582\u001b[0m resource_not_found \u001b[38;5;241m=\u001b[39m \u001b[38;5;124mf\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;132;01m{\u001b[39;00msep\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;132;01m{\u001b[39;00mmsg\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;132;01m{\u001b[39;00msep\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;124m\"\u001b[39m\n\u001b[1;32m--> 583\u001b[0m \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mLookupError\u001b[39;00m(resource_not_found)\n",
      "\u001b[1;31mLookupError\u001b[0m: \n**********************************************************************\n  Resource \u001b[93mpunkt\u001b[0m not found.\n  Please use the NLTK Downloader to obtain the resource:\n\n  \u001b[31m>>> import nltk\n  >>> nltk.download('punkt')\n  \u001b[0m\n  For more information see: https://www.nltk.org/data.html\n\n  Attempted to load \u001b[93mtokenizers/punkt/english.pickle\u001b[0m\n\n  Searched in:\n    - 'C:\\\\Users\\\\Jamie/nltk_data'\n    - 'c:\\\\Python311\\\\nltk_data'\n    - 'c:\\\\Python311\\\\share\\\\nltk_data'\n    - 'c:\\\\Python311\\\\lib\\\\nltk_data'\n    - 'C:\\\\Users\\\\Jamie\\\\AppData\\\\Roaming\\\\nltk_data'\n    - 'C:\\\\nltk_data'\n    - 'D:\\\\nltk_data'\n    - 'E:\\\\nltk_data'\n    - ''\n**********************************************************************\n"
     ]
    }
   ],
   "source": [
    "import nltk\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.stem import WordNetLemmatizer, PorterStemmer\n",
    "from nltk.tokenize import word_tokenize\n",
    "import re\n",
    "\n",
    "nltk.download('punkt')\n",
    "nltk.download('stopwords')\n",
    "nltk.download('wordnet')\n",
    "nltk.download('vader_lexicon')\n",
    "\n",
    "stop_words = set(stopwords.words('english'))\n",
    "lemmatizer = WordNetLemmatizer()\n",
    "stemmer = PorterStemmer()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def text_preprocessing(txt):\n",
    "    # Remove non-word characters and lowercase the text\n",
    "    txt = re.sub(r'\\W+', ' ', txt)\n",
    "    txt = txt.lower()\n",
    "\n",
    "    # Tokenize the text\n",
    "    word_tokens = word_tokenize(txt)\n",
    "\n",
    "    # Remove stop words\n",
    "    filtered_words = [w for w in word_tokens if w not in stop_words]\n",
    "\n",
    "    # Stem or Lemmatize each word\n",
    "    stemmed_words = [stemmer.stem(w) for w in filtered_words]\n",
    "    lemmatized_words = [lemmatizer.lemmatize(w) for w in stemmed_words]\n",
    "\n",
    "    # Join the words back into a single string\n",
    "    return ' '.join(lemmatized_words)\n",
    "\n",
    "# Apply the preprocessing function to the DataFrame\n",
    "df['original_text'] = df['Text']\n",
    "df['Text'] = df['Text'].apply(text_preprocessing)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Visualization"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Visualizing most frequent words\n",
    "from nltk.probability import FreqDist\n",
    "\n",
    "# Extracts words into list and count frequency\n",
    "all_words = ' '.join([text for text in df['Text']])\n",
    "all_words = all_words.split()\n",
    "words_df = FreqDist(all_words)\n",
    "\n",
    "# Extracting words and frequency from words_df object\n",
    "words_df = pd.DataFrame({'word':list(words_df.keys()), 'count':list(words_df.values())})\n",
    "\n",
    "# Subsets top 30 words by frequency\n",
    "words_df = words_df.nlargest(columns=\"count\", n = 30)\n",
    "\n",
    "words_df.sort_values('count', inplace = True)\n",
    "\n",
    "# Plotting 30 frequent words\n",
    "plt.figure(figsize=(20,10))\n",
    "plt.title(\"Top 50 Frequent Word\")\n",
    "ax = plt.barh(words_df['word'], width = words_df['count'])\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Training/Predicting"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from transformers import AutoModelForSequenceClassification\n",
    "from transformers import TFAutoModelForSequenceClassification\n",
    "from transformers import AutoTokenizer, AutoConfig\n",
    "import numpy as np\n",
    "from scipy.special import softmax\n",
    "\n",
    "MODEL = f\"cardiffnlp/twitter-roberta-base-sentiment-latest\"\n",
    "tokenizer = AutoTokenizer.from_pretrained(MODEL)\n",
    "config = AutoConfig.from_pretrained(MODEL)\n",
    "model = AutoModelForSequenceClassification.from_pretrained(MODEL)\n",
    "\n",
    "def get_sentiment(text):\n",
    "    # Tokenize the input text\n",
    "    encoded_input = tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=512)  # Pad and truncate to 3625 tokens)\n",
    "    \n",
    "    # Get model output\n",
    "    output = model(**encoded_input)\n",
    "    \n",
    "    # Calculate softmax scores\n",
    "    scores = output[0][0].detach().numpy()\n",
    "    scores = softmax(scores)\n",
    "\n",
    "    # Get the predicted label and its score\n",
    "    ranking = np.argsort(scores)\n",
    "    ranking = ranking[::-1]\n",
    "    predicted_label = config.id2label[ranking[0]]\n",
    "    predicted_score = scores[ranking[0]]\n",
    "\n",
    "    return predicted_label, predicted_score"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Sort the DataFrame by timestamp in descending order\n",
    "df = df.sort_values(by='Timestamp', ascending=False)\n",
    "\n",
    "# Get the latest 1000 rows\n",
    "latest_df = df.head(10)\n",
    "\n",
    "results = []\n",
    "for index, row in latest_df.iterrows():\n",
    "    text = row['original_text']\n",
    "    timestamp = row['Timestamp']\n",
    "    predicted_label, predicted_score = get_sentiment(text)\n",
    "    results.append([text, timestamp, predicted_label, predicted_score])\n",
    "\n",
    "    # Debugging information (optional)\n",
    "    print(f\"Text: {text}\")\n",
    "    print(f\"Timestamp: {timestamp}\")\n",
    "    print(f\"Predicted Label: {predicted_label}\")\n",
    "    print(f\"Predicted Score: {predicted_score}\\n\")\n",
    "\n",
    "# Create a Pandas DataFrame from the results\n",
    "results_df = pd.DataFrame(results, columns=['Original Text', 'Timestamp', 'Sentiment', 'Score'])\n",
    "\n",
    "results_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Top Frequent Mentioned Stocks\n",
    "\n",
    "# List of stocks to track\n",
    "stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'META', 'NVDA', 'CRWD']\n",
    "\n",
    "# Initialize a dictionary to store counts\n",
    "stock_counts = {stock: 0 for stock in stocks}\n",
    "\n",
    "# Iterate through the DataFrame and count mentions\n",
    "for _, row in results_df.iterrows():\n",
    "    text = row['Original Text'].lower()\n",
    "    for stock in stocks:\n",
    "        if stock.lower() in text:\n",
    "            stock_counts[stock] += 1\n",
    "\n",
    "# Create a Pandas Series from the counts\n",
    "stock_counts_series = pd.Series(stock_counts)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Sort the Series by count in descending order\n",
    "stock_counts_series = stock_counts_series.sort_values(ascending=False)\n",
    "\n",
    "# Plot the top N most frequently mentioned stocks\n",
    "N = 10  # Change this to the number of stocks you want to display\n",
    "plt.figure(figsize=(10, 6))\n",
    "stock_counts_series.head(N).plot(kind='bar')\n",
    "plt.xlabel('Stock')\n",
    "plt.ylabel('Frequency')\n",
    "plt.title('Top {} Frequently Mentioned Stocks'.format(N))\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "Stock_mention = ['CRWD', 'Crowdstrike', 'crowdstrike'] \n",
    "\n",
    "# Create a boolean mask for each word\n",
    "masks = [results_df['Original Text'].str.contains(word, case=False) for word in Stock_mention]\n",
    "\n",
    "# Combine the masks using logical OR\n",
    "combined_mask = np.logical_or.reduce(masks)\n",
    "\n",
    "# Filter the DataFrame using the combined mask\n",
    "filtered_df = results_df[combined_mask]\n",
    "\n",
    "# Display the filtered DataFrame\n",
    "filtered_df.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "positive_score_sum = filtered_df['Score'].where(filtered_df['Sentiment'] == 'positive').sum()\n",
    "negative_score_sum = filtered_df['Score'].where(filtered_df['Sentiment'] == 'negative').sum()\n",
    "neutral_score_sum = filtered_df['Score'].where(filtered_df['Sentiment'] == 'neutral').sum()\n",
    "\n",
    "data = [positive_score_sum, negative_score_sum, neutral_score_sum]\n",
    "Sentiments = ['Positive', 'Negative', 'Neutral']\n",
    " \n",
    "# Creating plot\n",
    "fig = plt.figure(figsize=(10, 5))\n",
    "plt.title('Sentiment Analysis on ' + (Stock_mention[0]))\n",
    "plt.pie(data, labels= Sentiments, autopct='%.2f')\n",
    " \n",
    "# show plot\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
