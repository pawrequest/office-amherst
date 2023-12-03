def test_boxes(hire_from_cmc, ot_auto):
    from office_am.merge_docs.box_label import box_labels_aio_tmplt

    box_pdf = box_labels_aio_tmplt(hire_from_cmc, ot_auto.doc)
    ...