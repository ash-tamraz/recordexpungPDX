import React from 'react';
import LogOut from '../LogOut';
import Logo from '../Logo';
import history from '../History';

class LoggedInHeader extends React.Component {
  public render() {
    return (
      // The following was copy/pasted directly from http://dev.huntermarcks.net/search/
      // and should be treated only as a draft.
      <nav className="center pt4 ph2 bg-white shadow">
        <div className="mw8 center flex-l justify-between">
          <div className="mb4">
            <Logo />
          </div>
          <div className="dib mb4">
            {/* These links aren't supposed to work right now. */}
            <button className="link hover-blue f6 f5-ns dib pa3">Search</button>
            <button className="link hover-blue f6 f5-ns dib pa3">Stats</button>
            <button className="link hover-blue f6 f5-ns dib pa3">Admin</button>
            <button className="link hover-blue f6 f5-ns dib pa3">
              Account
            </button>
            <LogOut>
              {/* Nesting the button within a <Link> tag here would
                render but creates invalid HTML.
                https://stackoverflow.com/questions/42463263/wrapping-a-react-router-link-in-an-html-button
              */}
              <button
                onClick={() => history.push('/')}
                className="link hover-blue f6 f5-ns dib pa3"
              >
                Log Out
              </button>
            </LogOut>
          </div>
        </div>
      </nav>
    );
  }
}

export default LoggedInHeader;
