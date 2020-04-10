
import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

class gatlingResponseTimeByIncreasingConcurrentUsers extends Simulation {

 val httpProtocol = http
    .baseUrl("http://127.0.0.1:30000")
    .acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    .doNotTrackHeader("1")
    .acceptLanguageHeader("en-US,en;q=0.5")
    .acceptEncodingHeader("gzip, deflate")
    .userAgentHeader("Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0")

  val scn = scenario("gatlingResponseTimeByIncreasingConcurrentUsers")
    .exec(http("request_1")
      .get("/"))
    .pause(5) 

  setUp(
    scn.inject(
		// Add 10 concurrent users 10 times with each level lasting 10 seconds
	    incrementConcurrentUsers(10) 
	      .times(10)
	      .eachLevelLasting(10 seconds)
	//      .separatedByRampsLasting(10 seconds)
    )
  ).protocols(httpProtocol) 
}
