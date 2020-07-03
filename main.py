from datetime import datetime, timedelta
import numpy as np
import functions as fn

test_date1 = datetime(year=2020, month=7, day=2)
test_date2 = datetime(year=2020, month=7, day=3)
df = fn.import_data(test_date1, test_date2)
fn.generate_html_code_last_measured_data()
fn.output_htmldiv_single_graph(df, 'Temperature1')
fn.output_htmldiv_single_graph(df, 'Temperature2')

fn.create_html_page('html_output/index.html',
                    fn.name_htmldiv_single_graph(df, 'Temperature1'),
                    fn.name_htmldiv_single_graph(df, 'Temperature2')
                    )
