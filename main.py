from class_xml import XML


def ratp_traffic():
   query = """
     for $ligne in //*:div[@class="encadre_ligne"]
       let $img := $ligne/*:img[1]
       let $a := $ligne//*:span[@class="perturb_link"]/*:a[1]
       return <result>
           <script>ratp_traffic</script>
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

   return XML(url="http://www.ratp.fr/meteo/").xquery(query)

for x in ratp_traffic():
  print(str(x))
