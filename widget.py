from altair import value
import rumps #ridiculously uncomplicated macos python statusbar apps
import subprocess #for running the streamlit app in the background
from tracker import build_dashboard_rows, format_money, format_percent

from datetime import datetime
from AppKit import NSApplication, NSApplicationActivationPolicyAccessory #hide python app from appearing in dock


#format_signed_money helper that I can't borrow from the other file because that applies colours which doesn't work in the menu bar widget
def format_signed_money(value): 
    if value > 0:
        return f"+${value:,.2f}"
    elif value < 0:
        return f"-${abs(value):,.2f}"
    else:
        return f"${value:,.2f}"

#format_signed_percentage helper that I can't borrow from the other file because that applies colours which doesn't work in the menu bar widget
def format_signed_percent(value): 
    if value > 0:
        return f"+{value:,.2f}%"
    elif value < 0:
        return f"-{abs(value):,.2f}%"
    else:
        return f"{value:,.2f}%"


#creates the menu bar widget, with options to show dash and quit
class ETFWidget(rumps.App):
    def __init__(self):
        super().__init__("ETF", quit_button=None) #sets the name of the menu bar widget to "ETF" and removes the default quit button since we will add our own in the menu
        
        #hide the python app from appearing in the dock
        NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyAccessory)

        self.refresh()

        self.timer = rumps.Timer(self.refresh_timer, 10)
        self.timer.start()

    def refresh_timer(self, _): #this function is called every 10 seconds by the timer to refresh the prices and menu
        self.refresh()    


    def refresh(self):

        try:
            rows = build_dashboard_rows()
        except Exception as error:
            last_updated = datetime.now().strftime("%I:%M:%S %p")

            self.title = "ETF: Error" #sets title of menu bar widget to show error if there is an issue with fetching prices
            self.menu.clear() #clear menu before repopulating
            self.menu.add(rumps.MenuItem(f"Error: {type(error).__name__}", callback=self.do_nothing))
            self.menu.add(rumps.MenuItem(f"Last tried: {last_updated}", callback=self.do_nothing))
            self.menu.add(None) #add a separator line in the menu
            self.menu.add(rumps.MenuItem("Refresh", callback=self.refresh_menu))
            self.menu.add(rumps.MenuItem("Quit", callback=self.quit_app))
            return

        portfolio_value = sum(row["current_value"] for row in rows)
        total_invested = sum(row["total_invested"] for row in rows)
        portfolio_return = portfolio_value - total_invested
        portfolio_return_percent = (portfolio_return / total_invested) * 100
        portfolio_day_change = sum(row["day_change"] for row in rows)
        portfolio_day_change_percent = (portfolio_day_change / (portfolio_value - portfolio_day_change)) * 100

        last_updated = datetime.now().strftime("%I:%M:%S %p")

        self.title = f"{format_signed_money(portfolio_day_change)}"

        self.menu.clear() #clear the menu before repopulating it with updated values

        self.menu.add(rumps.MenuItem(f"Invested: ${format_money(total_invested)}", callback=self.do_nothing))
        self.menu.add(rumps.MenuItem(f"Value: ${format_money(portfolio_value)}", callback=self.do_nothing))
        self.menu.add(rumps.MenuItem(f"ROI: {format_signed_money(portfolio_return)}" f" ({format_signed_percent(portfolio_return_percent)})", callback=self.do_nothing))
        self.menu.add(rumps.MenuItem(f"Day Change: {format_signed_money(portfolio_day_change)}" f" ({format_signed_percent(portfolio_day_change_percent)})", callback=self.do_nothing))


        self.menu.add(None) #add a separator line in the menu


        self.menu.add(rumps.MenuItem("Ticker        Price      Day %       ROI %   Weight", callback=self.do_nothing)) #add a header line for the holdings section of the menu
        self.menu.add(None)

        for row in rows:
            line = (
                f"{row['ticker']:<8} "
                f"{row['current_price']:>8.2f} "
                f"{row['day_change_percent']:>+7.2f}% "
                f"{row['total_return_percent']:>+9.2f}% "
                f"{row['weight_percent']:>7.2f}%"
            )
            self.menu.add(rumps.MenuItem(line, callback=self.do_nothing))
        

        self.menu.add(None) #add a separator line in the menu


        self.menu.add(rumps.MenuItem(f"Last updated: {last_updated}", callback=self.do_nothing)) #add the last updated time at the bottom of the menu
        
        self.menu.add(None) #add another separator line
        
        self.menu.add(rumps.MenuItem("Show Full Dashboard", callback=self.show_dashboard)) #add an option to show the dashboard
        self.menu.add(rumps.MenuItem("Refresh", callback=self.refresh_menu)) #add an option to refresh prices
        self.menu.add(rumps.MenuItem("Quit", callback=self.quit_app)) #add an option to quit the app


    #when refresh is clicked, call the refresh function to update the prices and menu
    def refresh_menu(self, _):
        self.refresh()

    #when quit is clicked, quit the app (normally built in, but refresh is wipes it so we add it back in here)
    def quit_app(self, _):
        rumps.quit_application()

    def show_dashboard(self, _):
        subprocess.Popen([".venv/bin/streamlit", "run", "app.py"],
                         cwd="/Users/timothyxiao/Library/CloudStorage/OneDrive-TheUniversityofMelbourne/Projects/etf-dashboard",
        )
    def do_nothing(self, _):
        pass

if __name__ == "__main__":
    ETFWidget().run()