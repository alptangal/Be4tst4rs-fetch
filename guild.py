import asyncio


async def getBasic(guild):
    usernamesCh,usernames,threads,threadsCh,contentsCh,password,contents,logsCh=None,None,None,None,None,None,None,None
    for category in guild.categories:
        if 'beatstars' in category.name.lower():
            for channel in category.channels:
                if 'usernames' in channel.name:
                    usernamesCh = channel
                    usernames = [msg async for msg in channel.history()]
                elif 'password' in channel.name:
                    password = [msg async for msg in channel.history()][0].content
                elif 'threads' in channel.name:
                    threadsCh = channel
                    threads = channel.threads
                    threads += [thread async for thread in channel.archived_threads()]
                elif 'contents' in channel.name:
                    contentsCh = channel
                    contents = channel.threads
                    contents += [thread async for thread in channel.archived_threads()]
                elif 'logs' in channel.name:
                    logsCh = channel
    return {'usernamesCh': usernamesCh, 'usernames': usernames, 'password': password, 'threadsCh': threadsCh, 'threads': threads, 'contentsCh': contentsCh, 'contents': contents,'logsCh':logsCh}
