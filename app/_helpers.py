from flask import flash

def to_bool(n):
    if n == 0:
        return False
    else:
        return True

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))