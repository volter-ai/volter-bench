import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let BaseCard = withClickable(Card)
let BaseCardHeader = withClickable(CardHeader)
let BaseCardContent = withClickable(CardContent)
let BaseCardTitle = withClickable(CardTitle)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <BaseCard ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
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
