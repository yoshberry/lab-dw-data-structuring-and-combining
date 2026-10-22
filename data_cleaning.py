
import pandas as pd


def clean_column_names(customer_data):
    customer_data.columns = customer_data.columns.str.lower().str.replace(" ", "_")
    customer_data = customer_data.rename(columns={"st": "state"})

    return customer_data


def clean_invalid_values(customer_data):
    customer_data["gender"] = customer_data["gender"].replace({
        "Femal": "F",
        "female": "F",
        "Male": "M"
    })

    customer_data["state"] = customer_data["state"].replace({
        "AZ": "Arizona",
        "Cali": "California",
        "WA": "Washington"
    })

    customer_data["education"] = customer_data["education"].replace({
        "Bachelors": "Bachelor"
    })

    customer_data["customer_lifetime_value"] = (
        customer_data["customer_lifetime_value"].str.replace("%", "", regex=False)
    )

    customer_data["vehicle_class"] = customer_data["vehicle_class"].replace({
        "Sports Car": "Luxury",
        "Luxury SUV": "Luxury",
        "Luxury Car": "Luxury"
    })

    return customer_data


def format_data_types(customer_data):
    customer_data["customer_lifetime_value"] = pd.to_numeric(
        customer_data["customer_lifetime_value"]
    )

    customer_data["number_of_open_complaints"] = (
        customer_data["number_of_open_complaints"].str.split("/").str[1]
    )

    customer_data["number_of_open_complaints"] = pd.to_numeric(
        customer_data["number_of_open_complaints"]
    )

    return customer_data


def handle_missing_values(customer_data):
    customer_data = customer_data.dropna(how="all")

    customer_data["gender"] = customer_data["gender"].fillna(
        customer_data["gender"].mode()[0]
    )

    customer_data["customer_lifetime_value"] = (
        customer_data["customer_lifetime_value"].fillna(
            customer_data["customer_lifetime_value"].median()
        )
    )

    numeric_columns = customer_data.select_dtypes(include="number").columns

    customer_data[numeric_columns] = customer_data[numeric_columns].astype(int)

    return customer_data


def remove_duplicates(customer_data):
    customer_data = customer_data.drop_duplicates()
    customer_data = customer_data.reset_index(drop=True)

    return customer_data


def main():
    url = "https://raw.githubusercontent.com/data-bootcamp-v4/data/main/file1.csv"

    customer_data = pd.read_csv(url)

    customer_data = clean_column_names(customer_data)
    customer_data = clean_invalid_values(customer_data)
    customer_data = format_data_types(customer_data)
    customer_data = handle_missing_values(customer_data)
    customer_data = remove_duplicates(customer_data)

    customer_data.to_csv("customer_data_cleaned.csv", index=False)

    return customer_data


if __name__ == "__main__":
    main()
