import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

let BaseCard = Card
let BaseCardContent = CardContent
let BaseCardHeader = CardHeader
let BaseCardTitle = CardTitle

BaseCard = withClickable(BaseCard)
BaseCardContent = withClickable(BaseCardContent)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardTitle = withClickable(BaseCardTitle)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
      <BaseCardHeader uid={`${uid}-header`}>
        <BaseCardTitle uid={`${uid}-title`}>{name}</BaseCardTitle>
      </BaseCardHeader>
      <BaseCardContent uid={`${uid}-content`}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </BaseCardContent>
    </BaseCard>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
