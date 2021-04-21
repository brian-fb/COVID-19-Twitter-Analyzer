
import jsonlines
from datetime import datetime
from datetime import timedelta

def date_convertor(file_id):
    now_date = datetime.strptime('20200418','%Y%m%d').date()
    offset_date = timedelta(days=file_id-31)
    return (now_date + offset_date).strftime('%Y-%m-%d')


def state_convert_to_abbrev(name,state_abbrev_df):
    try:
        abbrev = state_abbrev_df.loc[name]['Abbreviation']
    except:
        abbrev = 'unknown'
    return abbrev

def find_state_abbrev(place_info,state_abbrev_df):
    city_info = place_info.get('full_name')
    if ',' in city_info:
        state = city_info.split(',')[1].strip(' ')
        if state == 'USA':
            state = state_convert_to_abbrev(city_info.split(',')[0].strip(' '),state_abbrev_df)
        elif len(state)>2 :
            state = state_convert_to_abbrev(state,state_abbrev_df)
    else:
        state = 'unknown'
    return state

def len_jsonl(filename):
    count = 0
    with jsonlines.open(filename) as reader:
        for line in reader:
            count += 1
    return count

if __name__ == '__main__':
  print(0)