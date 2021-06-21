**This project is in no way associated with LernSax, WebWeaver, DigiOnline GmbH or Freistaat Sachsen**

## What is this?
This is an API Wrapper for the LernSax API using requests. Please note that I do not encourage taking any harmful actions against anyone using this wrapper.

## Documentation?
There is no documentation just yet. However I would refer you to [this repo](https://github.com/TKFRvisionOfficial/lernsax-webweaver-api-research) for getting a hang of the API.

## Example Usage
```
import lernsax

client = lernsax.Client()
client.login("realmail@lernsax.de", "gutePass")
print(client.get_emails("494e424f58"))
```

## WebDAV?
Instead of maintaining the sync version of LernSax.py I will focus on completing the async branch which will have WebDAV access to implement a nicer way to read-/write files
