import apiService, { Request } from './api-service';

describe('API SERVICE TEST', () => {
  it('returns data with get', () => {
    const request: Request = {
      url: 'http://localhost:5000/api/hello',
      method: 'get'
    };
    apiService(request).then((response: any) => {
      expect(response).toEqual({
        data: 'Hello, world!'
      });
    });
  });

  it('returns with error on bad base url', done => {
    const request: Request = {
      url: 'http://:5000/api/',
      method: 'get'
    };
    apiService(request).catch((error: any) => {
      expect(error.error.message).toEqual(
        'bad base url, it should be: http://localhost:5000/api/'
      );
      done();
    });
  });

  it('returns with 404 error on bad route', done => {
    const request: Request = {
      url: 'http://localhost:5000/api/ello',
      method: 'get'
    };
    apiService(request).catch((error: any) => {
      expect(error.error.message).toEqual(
        'Request failed with status code 404'
      );
      done();
    });
  });

  it('returns search in JSON', done => {
    const request: Request = {
      url: 'http://localhost:5000/api/search',
      method: 'post'
    };
    apiService(request).then((response: any) => {
      expect(response).toEqual({
        data: [
          {
            name: 'WOODS, LAVELLE D',
            birth_year: 1970,
            case_number: 'ZA0081909',
            citation_number: 'ZA0081909',
            location: 'Multnomah',
            date: '07/02/2013',
            violation_type: 'Offense Violation',
            current_status: 'Inactive',
            balance_due: '0',
            charges: [
              {
                name: 'Failure to Properly Use Safety Belts - MV Operator',
                statute: '8112101A',
                level: 'Violation Class D',
                date: '06/11/2013',
                disposition: {
                  date: '07/16/2013',
                  ruling: 'Convicted'
                },
                expungement_result: {
                  type_eligibility: 'True',
                  type_eligibility_reason: 'some string',
                  time_eligibility: 'True',
                  time_eligibility_reason: 'some string',
                  date_of_eligibility: 'date'
                }
              }
            ],
            case_detail_link:
              'https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=9036658'
          }
        ]
      });
      done();
    });
  });
});
