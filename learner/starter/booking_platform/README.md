# Booking Platform Starter

Small dependency-free Python codebase for the Day 4 inherited-system exercise. See `policy/business_rules.md` for approved training policy. Source code reflects historical behavior and may drift from policy. Run baseline tests with:

```bash
python3 -m unittest discover -s tests -v
```

The public functions used by the training exercise are `src.api.create_quote(rooms)` and `src.invoice.preview_invoice(rooms)`. Keep their argument and return shapes stable during the refactor.
