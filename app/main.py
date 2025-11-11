from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, abort
from flask_login import login_required, current_user
from app import db
from app.models import Task
from app.forms import TaskForm  # Importez le nouveau formulaire
import openpyxl
from io import BytesIO

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required # Sécurise cette route
def index():
    # Créez une instance du formulaire d'ajout de tâche
    form = TaskForm()
    
    # --- LOGIQUE D'AJOUT DE TÂCHE (remplace le commentaire) ---
    if form.validate_on_submit():
        # Crée une nouvelle tâche en l'associant à l'utilisateur actuel
        task = Task(title=form.title.data, 
                    description=form.description.data, 
                    author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Nouvelle tâche ajoutée !', 'success')
        return redirect(url_for('main.index')) # Redirige pour éviter de re-soumettre

    # --- LOGIQUE D'AFFICHAGE (GET) ---
    # Récupère toutes les tâches de l'utilisateur connecté
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.status).all()
    
    # Rend le template, en lui passant les tâches ET le formulaire
    return render_template('index.html', tasks=tasks, form=form)


# --- ROUTE POUR MARQUER UNE TÂCHE COMME TERMINÉE ---
@bp.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    # Récupère la tâche ou renvoie une erreur 404
    task = Task.query.get_or_404(task_id)
    
    # Vérifie que la tâche appartient bien à l'utilisateur connecté (Sécurité)
    if task.author != current_user:
        abort(403) # Erreur "Forbidden"
        
    task.status = 'done'
    db.session.commit()
    flash('Tâche marquée comme terminée.', 'info')
    return redirect(url_for('main.index'))


# --- ROUTE POUR SUPPRIMER UNE TÂCHE ---
@bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
        
    db.session.delete(task)
    db.session.commit()
    flash('Tâche supprimée.', 'info')
    return redirect(url_for('main.index'))


# --- ROUTE D'EXPORT EXCEL (inchangée) ---
@bp.route('/export/excel')
@login_required
def export_excel():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.status).all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Mes Tâches"
    ws.append(["Titre", "Description", "Statut"])

    for task in tasks:
        ws.append([task.title, task.description, task.status])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return Response(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": "attachment;filename=rapport_taches.xlsx"}
    )