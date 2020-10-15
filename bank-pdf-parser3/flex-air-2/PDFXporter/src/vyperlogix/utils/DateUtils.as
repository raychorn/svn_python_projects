package vyperlogix.utils {
	public class DateUtils {
		public static function epoch_now():Number {
			var now:Date = new Date();
			var epoch:Number = Date.UTC(now.fullYear, now.month, now.date, now.hours, now.minutes, now.seconds, now.milliseconds);
			return epoch;
		}
	}
}