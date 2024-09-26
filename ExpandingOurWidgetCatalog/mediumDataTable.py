import ui
import json
from datetime import date, datetime


class Data:  # TableView data_source
  def __init__(self, json_file):
    self.json_file = json_file
    with open(json_file, 'r') as f:
      self.data = json.load(f)
      
  def save_data(self):
    with open(self.json_file, 'w') as f:
      json.dump(self.data, f)

  # define the methods required by
  # the protocol defined for a data_source       
  
  def tableview_number_of_rows(self, tableview, section):
    # Return the number of rows in the section
    v['count'].text = str(len(self.data))
    return len(self.data)

  def tableview_cell_for_row(self, tableview, section, row):
    # Create and return a cell for the given section/row
    cell = ui.TableViewCell(style='subtitle')
    cell.text_label.text = self.data[row]['name']
    cell.detail_text_label.text = self.data[row]['birthdate']
    cell.accessory_type = 'none'
    return cell

  def tableview_delete(self, tableview, section, row):
    # Called when the user confirms deletion of the given row.
    del(self.data[row])
    tab.reload_data()

  def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
    # Called when the user moves a row with the reordering control (in editing mode).
    row = self.data[from_row].copy()
    del(self.data[from_row]) 
    self.data.insert(to_row, row) 
    tab.reload_data()
  
  # boilerplate methods required by
  # the data_source, but not used in
  # our example
  def tableview_number_of_sections(self, tableview):
    # Return the number of sections (defaults to 1)
    return 1
      
  def tableview_title_for_header(self, tableview, section):
    # Return a title for the given section.
    # If this is not implemented, no section headers will be shown.
    return ''

  def tableview_can_delete(self, tableview, section, row):
    # Return True if the user should be able to delete the given row.
    return True

  def tableview_can_move(self, tableview, section, row):
    # Return True if a reordering control should be shown for the given row (in editing mode).
    return True
    
    
class FanDelegate:  # delegate methods used by TableView
  def tableview_did_select(self, tableview, section, row):
    # Called when a row was selected.
    # we will open a view to edit the row
    ev['nameField'].text = ds.data[row]['name']
    ev['birthdateField'].date = datetime.strptime(ds.data[row]['birthdate'], '%Y-%m-%d')
    ev['birthdateField'].mode = ui.DATE_PICKER_MODE_DATE
    ev['emailField'].text = ds.data[row]['email']
    ev['addOrEdit'].text = 'Edit Fan'
    v['saveEditRow'].text = str(row)
    nv.navigation_bar_hidden = False
    nv.background_color = 'white'
    nv.push_view(ev)

  def tableview_did_deselect(self, tableview, section, row):
    # Called when a row was de-selected (in multiple selection mode).
    # we wont be using this in our example
    pass

  def tableview_title_for_delete_button(self, tableview, section, row):
    # Return the title for the 'swipe-to-***' button.
    return 'Delete'
    
    
def newFan(sender):
  ev['nameField'].text = ''
  ev['birthdateField'].date = date.today()
  ev['birthdateField'].mode = ui.DATE_PICKER_MODE_DATE
  ev['emailField'].text = ''
  ev['addOrEdit'].text = 'Add Fan'
  v['saveEditRow'].text = '-1'
  nv.navigation_bar_hidden = False
  nv.push_view(ev)
  
def saveFan(sender):
  fan = {'name': ev['nameField'].text,
    'birthdate': ev['birthdateField'].date.strftime('%Y-%m-%d'),
    'email': ev['emailField'].text}
  row = int(v['saveEditRow'].text)
  if row >= 0:
    ds.data[row] = fan
  else:
    ds.data.append(fan)
  tab.reload_data()
  nv.navigation_bar_hidden = True
  nv.pop_view()
  
def cancelFan(sender):
  tab.reload_data()
  nv.navigation_bar_hidden = True
  nv.pop_view()
  
def toggleEditing(sender):
  if tab.editing:
    tab.set_editing(False, True)
  else:
    tab.set_editing(True, True)
    
def saveList(sender):
  ds.save_data()
  

# Main body of program   
v = ui.load_view('mediumTableView.pyui')
v.flex = 'WHLRTB'
v.background_color = 'white'
v.name = 'Python Library Fan Club'
nv = ui.NavigationView(v)
nv.bar_tint_color = 'white'
nv.navigation_bar_hidden = True

tab = v['fanTable'] # streamline access to table
ds = tab.data_source = Data('mediumData.json') # add our data_source
tab.delegate = FanDelegate()
tab.reload()

ev = ui.load_view('editRow.pyui')

nv.present('sheet')
