import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let BaseCard = Card
let BaseCardContent = CardContent
let BaseCardHeader = CardHeader
let BaseCardTitle = CardTitle

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => {
    return (
      <BaseCard ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
        <BaseCardHeader uid={uid}>
          <BaseCardTitle uid={uid}>{name}</BaseCardTitle>
        </BaseCardHeader>
        <BaseCardContent uid={uid}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-cover rounded-md"
          />
        </BaseCardContent>
      </BaseCard>
    )
  }
)

PlayerCard.displayName = "PlayerCard"

BaseCard = withClickable(BaseCard)
BaseCardContent = withClickable(BaseCardContent)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardTitle = withClickable(BaseCardTitle)
PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
