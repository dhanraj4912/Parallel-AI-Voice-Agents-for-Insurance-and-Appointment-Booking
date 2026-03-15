def apply_discount(doctors):

    discount = 0.2

    for doc in doctors:

        doc["discounted_fee"] = int(doc["fees"]*(1-discount))

    return doctors