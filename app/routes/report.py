from urllib import request

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user

from ..extensions import db
from ..models.report import Report

report = Blueprint('report', __name__)
