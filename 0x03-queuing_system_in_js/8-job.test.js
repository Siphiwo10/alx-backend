import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';
import { expect } from 'chai';

describe('createPushNotificationsJobs', () => {
  let queue;

  // Set up the queue in test mode before tests run
  beforeEach(() => {
    queue = kue.createQueue({
      redis: 'redis://127.0.0.1:6379',  // Adjust this URL if necessary
    });
    queue.testMode = true; // Enter test mode, jobs won't be processed
  });

  // Clear the queue and exit test mode after tests
  afterEach((done) => {
    queue.testMode = false;  // Exit test mode after tests are done
    queue.remove({ type: 'push_notification_code_3' }, done); // Clear the queue
  });

  it('should throw an error if jobs is not an array', () => {
    const invalidJobs = 'not an array';
    expect(() => createPushNotificationsJobs(invalidJobs, queue)).to.throw('Jobs is not an array');
  });

  it('should create two new jobs in the queue', (done) => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'Test message 1' },
      { phoneNumber: '4153518781', message: 'Test message 2' },
    ];

    createPushNotificationsJobs(jobs, queue);

    // Validate that jobs are inside the queue but not processed
    setImmediate(() => {
      const jobIds = queue.testMode.jobs.map(job => job.id);
      expect(jobIds.length).to.equal(2);
      expect(jobIds).to.include.members([1, 2]); // Check that jobs 1 and 2 exist
      done();
    });
  });

  it('should not process the jobs in test mode', (done) => {
    const jobs = [
      { phoneNumber: '4153518782', message: 'Test message 3' },
      { phoneNumber: '4153518783', message: 'Test message 4' },
    ];

    createPushNotificationsJobs(jobs, queue);

    // Check that jobs are not processed (no progress, no completion)
    setImmediate(() => {
      const job = queue.testMode.jobs.find(job => job.id === 3);
      expect(job).to.exist;
      expect(job._progress).to.equal(0); // Jobs should not have progressed
      done();
    });
  });
});

