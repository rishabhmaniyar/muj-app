import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from .FiveWrapper import *
from .models import Levels
from datetime import datetime

login_client = loginUser()
positions_instance = positions()
ltpClient = ltp()


# create_track_map = {}


@method_decorator(csrf_exempt, name='dispatch')
class LevelsView(View):
    def get(self, request):
        try:
            levels = Levels.objects.filter(isActive=True).all()
            level_list = [
                {
                    'symbol': level.symbol,
                    'option_type': level.option_type,
                    'transaction_type': level.transaction_type,
                    'expiry': level.expiry,
                    'strike': level.strike,
                    'qty': level.qty,
                    'underlying_price': level.underlying_price,
                    'option_price': level.option_price,
                    'sl_price': level.sl_price,
                    'underlying_sl_price': level.underlying_sl_price,
                    'target_price': level.target_price,
                    'underlying_target_price': level.underlying_target_price,
                    'isActive': level.isActive
                }
                for level in levels
            ]
            return JsonResponse(level_list, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    def post(self, request):
        try:
            data = json.loads(request.body)
            symbol = data.get('symbol')

            # Check if the level exists
            existing_level = Levels.objects.filter(symbol=symbol, isActive=True).first()

            if existing_level:
                # If level exists, mark it as inactive
                existing_level.isActive = False
                existing_level.save()

            # Create new level
            new_level = Levels(**data)
            new_level.save()

            return JsonResponse({"message": "Saved new level successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    def put(self, request):
        try:
            data = json.loads(request.body)
            symbol = data.get('symbol')

            # Check if the level exists
            existing_level = Levels.objects.filter(symbol=symbol).first()

            if existing_level:
                # Update existing level
                for key, value in data.items():
                    setattr(existing_level, key, value)
                existing_level.save()
                return JsonResponse({"message": "Updated level successfully"}, status=200)
            else:
                return JsonResponse({"message": "Level not found"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)


create_track_map = {}


@csrf_exempt
def start_tracking(request):
    if request.method == 'GET':
        try:
            symbol = request.GET.get('symbol')

            if create_track_map is None or create_track_map == {}:
                create_tracker(request)
            # Fetch the last active level by symbol
            existing_level = Levels.objects.filter(symbol=symbol, isActive=True).last()

            if existing_level:
                # Perform operations on existing_level here
                symbol = existing_level.symbol
                print("Ex price to track", existing_level.underlying_price)
                client = login_client.login_token()
                # res = positions_instance.fetch_positions(client=client)
                newMap=create_track_map[symbol]
                for k in list(newMap):
                    print("Key ", k)
                    # print("Value ", newMap[k])
                    ltp = ltpClient.fetch_underlying_ltp(client=client, underlyingName=list(newMap)[0],optionName=list(newMap)[1])
                    print("LTP: ", ltp)

                return JsonResponse({"message": "Operations performed successfully on the last active level"},
                                    status=200)
            else:
                return JsonResponse({"message": "No active level found for the provided symbol"}, status=404)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Only GET method is allowed for this endpoint"}, status=405)


def getDateFormatted(expiry):
    date_obj = datetime.strptime(expiry, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d %b %Y")
    return formatted_date


@csrf_exempt
def create_tracker(request):
    if request.method == 'GET':
        try:
            # Fetch the last active level by symbol
            existing_level = Levels.objects.filter(isActive=True).all()

            if existing_level:
                # Perform operations on existing_level here
                for level in existing_level:
                    symbol = level.symbol
                    optionsSymbol = symbol + " " + getDateFormatted(
                        level.expiry) + " " + level.option_type + " " + level.strike + ".00"
                    print("Ex Symbol to track", symbol, "options Symbol is -> ", optionsSymbol)
                    spot_info = [level.underlying_price, (level.underlying_sl_price, level.underlying_target_price)]
                    options_info = [level.option_price, (level.sl_price, level.target_price)]

                    # Add symbol with spot and options info to the track map
                    create_track_map[symbol] = {symbol: spot_info, optionsSymbol: options_info}

                return JsonResponse({"message": create_track_map},
                                    status=200)
            else:
                return JsonResponse({"message": "No active level found for the provided symbol"}, status=404)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Only GET method is allowed for this endpoint"}, status=405)
