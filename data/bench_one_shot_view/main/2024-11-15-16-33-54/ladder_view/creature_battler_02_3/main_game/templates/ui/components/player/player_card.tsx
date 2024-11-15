import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let BaseCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
      <CardHeader uid={uid}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      </CardHeader>
      <CardContent uid={uid}>
        <h3 className="text-lg font-bold text-center">{name}</h3>
      </CardContent>
    </Card>
  )
)

BaseCard.displayName = "PlayerCard"

let PlayerCard = withClickable(BaseCard)

export { PlayerCard }
