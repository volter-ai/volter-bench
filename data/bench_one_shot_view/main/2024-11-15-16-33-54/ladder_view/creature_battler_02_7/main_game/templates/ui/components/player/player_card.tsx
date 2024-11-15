import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let BaseCard = Card
let BaseCardHeader = CardHeader
let BaseCardContent = CardContent

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
      <BaseCardHeader uid={`${uid}-header`}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-48 object-cover rounded-t-xl"
        />
      </BaseCardHeader>
      <BaseCardContent uid={`${uid}-content`}>
        <h3 className="text-lg font-bold text-center">{name}</h3>
      </BaseCardContent>
    </BaseCard>
  )
)

PlayerCard.displayName = "PlayerCard"

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardContent = withClickable(BaseCardContent)
PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
