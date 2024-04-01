from flask import jsonify, Blueprint, request, make_response
from data.db_session import create_session
from data.jobs import Jobs
import datetime

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict()
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = create_session()
    jobs = Jobs()
    jobs.team_leader = request.json['team_leader']
    jobs.job = request.json['job']
    jobs.work_size = request.json['work_size']
    jobs.collaborators = request.json['collaborators']
    jobs.start_date = datetime.datetime.fromisoformat(request.json['start_date'])
    jobs.end_date = datetime.datetime.fromisoformat(request.json['end_date'])
    jobs.is_finished = request.json['is_finished']
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    db_sess = create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job:
        return jsonify(
            {
                'job': job.to_dict()
            }
        )
    return jsonify(
        {
            'error': f'no job with id={job_id}'
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_jobs(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(
            key in request.json for key in
            ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']
            ):
        return jsonify({'error': 'Bad request'})
    db_sess = create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify(
            {'error': 'Not found'}
        )
    db_sess.delete(job)
    job.team_leader = request.json['team_leader']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    db_sess.add(job)
    db_sess.commit()
    return jsonify(
        {
            'edited_job': job.to_dict()
        }
    )
