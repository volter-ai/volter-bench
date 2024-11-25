import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as BaseCard, CardHeader as BaseCardHeader, CardContent as BaseCardContent } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

let Card = withClickable(BaseCard)
let CardHeader = withClickable(BaseCardHeader)
let CardContent = withClickable(BaseCardContent)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
      <CardHeader uid={`${uid}-header`}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      </CardHeader>
      <CardContent uid={`${uid}-content`}>
        <h3 className="text-lg font-bold text-center">{name}</h3>
      </CardContent>
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
