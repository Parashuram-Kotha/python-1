from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

class ExpenseApp(App):
    def build(self):
        self.expenses = {}  # Store categories and expenses
        
        layout = BoxLayout(orientation='vertical')
        form_layout = GridLayout(cols=2)

        # Date input
        form_layout.add_widget(Label(text="Date (YYYY-MM-DD):"))
        self.date_input = TextInput(multiline=False)
        form_layout.add_widget(self.date_input)

        # Category dropdown
        form_layout.add_widget(Label(text="Category:"))
        self.category_input = Spinner(
            text='Food', values=('Food', 'Transport', 'Rent', 'Other')
        )
        form_layout.add_widget(self.category_input)

        # Amount input
        form_layout.add_widget(Label(text="Amount:"))
        self.amount_input = TextInput(multiline=False, input_filter='float')
        form_layout.add_widget(self.amount_input)

        # Add expense button
        submit_btn = Button(text="Add Expense")
        submit_btn.bind(on_press=self.add_expense)
        form_layout.add_widget(submit_btn)

        # Add new category button
        add_category_btn = Button(text="Add Category")
        add_category_btn.bind(on_press=self.add_category)
        form_layout.add_widget(add_category_btn)

        layout.add_widget(form_layout)

        # Display expenses
        self.expense_display = BoxLayout(orientation="vertical")
        layout.add_widget(self.expense_display)

        return layout

    def add_expense(self, instance):
        date = self.date_input.text
        category = self.category_input.text
        amount = self.amount_input.text

        # Basic Validation
        if date and category and amount:
            if category not in self.expenses:
                self.expenses[category] = []
            self.expenses[category].append({'date': date, 'amount': amount})

            self.expense_display.clear_widgets()
            for cat, expense_list in self.expenses.items():
                for exp in expense_list:
                    self.expense_display.add_widget(Label(text=f"{exp['date']} - {cat} - ${exp['amount']}"))
        else:
            print("All fields are required!")

    def add_category(self, instance):
        popup_content = TextInput(hint_text="Enter new category")
        confirm_button = Button(text="Confirm")
        popup_layout = GridLayout(cols=1)
        popup_layout.add_widget(popup_content)
        popup_layout.add_widget(confirm_button)

        popup = Popup(title="Add New Category", content=popup_layout, size_hint=(0.75, 0.5))

        def on_confirm(instance):
            new_category = popup_content.text.strip()
            if new_category:
                # Update Spinner values
                self.category_input.values = (*self.category_input.values, new_category)
                print(f"Added new category: {new_category}")
            popup.dismiss()

        confirm_button.bind(on_press=on_confirm)
        popup.open()

if __name__ == "__main__":
    ExpenseApp().run()
