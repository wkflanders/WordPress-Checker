import pandas as pd

confirmed_df = pd.read_csv('confirmed_sites.csv')
output_df = pd.read_csv('output_sites.csv')

validation_sites = set(confirmed_df['URL'])
test_sites = set(output_df['URL'])

unique_test_sites = test_sites - validation_sites

unique_test_sites_df = pd.DataFrame(list(unique_test_sites), columns=['URL'])

print(unique_test_sites_df)
print(len(unique_test_sites))