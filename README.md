# stocks

When I think about stock options I feel dumb. It's too complicated for someone who has MS in Computer Science...

This script assists me with building my exercising and selling plans. If you are working in a startup company - this will be quite handy.

The script reads a JSON config file which describes your stock situation and prints out info such as:
- how much would you pay for taxes for ISO or NSO type of stocks
- how much would you pay immediately
- how much would you get in cash

It doesn't calculate Alternative Minimum Tax (AMT) as I have no idea how it works. **Would be awesome if someone adds that part.**

The config file has three parts in it:

##### stocks
Here you describe your stock situation. You can specify the grant_date, stock_type (ISO, NSO), count, strike_price, vesting_period.

##### exercise
Here you can specify verious exercising scenarios. This is very useful since it helps you understand when and how you will benefit if you take a certain action.
You can specify exercise_date, stock_type, number of stocks to exercise ("AllVested" means all vested stocks), future price.

##### sell
This one is currently quite simple. You specify a date, future price and it calculates how much your stocks are worth. If you want to get excited - put a big number of future price...
