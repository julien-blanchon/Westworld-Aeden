# Westworld-Aeden
A simple Aeden (from https://discoverwestworld.com/?forceus) bot.

## Getting Started

aeden.py will try all the words of your database and get the answer.

### Prerequisites:

You just need python2 and 2 packages:

Python 2 (with pip): ```sudo apt-get -y install python python-pip python-dev build-essential```
Python Websocket-client: ```sudo pip install websocket-client```
Python Request: ```sudo pip install requests```

You can also use the requirements.txt file: ```sudo pip install -r requirements.txt```

### Installation:

Clone the repository just exec install.sh ```./install.sh``` (It will install all the requirement)

#### Fast instal:
	``` sudo apt-get update
		sudo apt-get -y install git git-core python python-pip python-dev build-essential
		git clone git://github.com/julien-blanchon/Westworld-Aeden.git
		cd Westworld-Aeden/
		sudo pip install -r requirements.txt
		```

### Use:

```python aeden.py <txt file to text> <csv file to save>```

And if you want ```python aeden.py <txt file to text> <csv file to save> >> <file to save all log>```