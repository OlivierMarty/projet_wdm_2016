from class_xml import XML
import config

def ratp_traffic():
  query = """
     for $ligne in //*:div[@class="encadre_ligne"]
       let $img := $ligne/*:img[1]
       let $a := $ligne//*:span[@class="perturb_link"]/*:a[1]
       return <result>
           <source>ratp_traffic</source>
           <id>ratp_traffic_{ data($ligne/@id) }</id>
           <status>
           {
             if ($img/@alt = "normal")
             then "ok"
             else "problem"
           }
           </status>
           <images>
             <img src="http://ratp.fr{ $img/@src }" alt="{ $img/@alt }"/>
           </images>
           <message>
           {
             $ligne//*:span[@class="perturb_message"]/text()
           }
           </message>
           <links>
           {
             if ($a/@href="")
             then ""
             else <a href="{ $a/@href }">{ $a/text() }</a>
           }
           </links>
         </result>
     """

  return XML(url="http://www.ratp.fr/meteo/", lang="html").xquery(query)

def jcdecaux_vls():
  query = """
     (: TODO bug de fuseau horaire :)
     (:~ convert epoch seconds to dateTime :)
     declare function local:millitimestamp-to-date($v) as xs:string
     {
       let $len := string-length($v)
       let $timestamp := substring($v, 1, $len - 3)
       let $datetime := xs:dateTime("1970-01-01T00:00:00-00:00") + xs:dayTimeDuration(concat("PT", $timestamp, "S"))
       return format-dateTime($datetime, "à [H01]h[M01] le [D01]/[M01]", "en", "AD", "fr")
     };
     
     for $res in /*:json/*:item
       let $places := $res/*:available_bike_stands/text()
       return <result>
           <source>jcdecaux_vls</source>
           <id>jcdecaux_vls_{ $res/*:number/text() }</id>
           {
             if ($places > 4)
             then <status>ok</status>
             else (
                 <status>problem</status>,
                 <message>Station vélo { lower-case($res/*:name/text()) } : { local:millitimestamp-to-date($res/*:last_update/text()) } : plus que { $places } places disponibles !</message>
               )
           }
         </result>
     """

  return XML(url="https://api.jcdecaux.com/vls/v1/stations?contract=paris&apiKey="+config.api_key['jcdecaux'], lang="json").xquery(query)

for x in ratp_traffic():
  print(str(x))
for x in jcdecaux_vls():
  print(str(x))
