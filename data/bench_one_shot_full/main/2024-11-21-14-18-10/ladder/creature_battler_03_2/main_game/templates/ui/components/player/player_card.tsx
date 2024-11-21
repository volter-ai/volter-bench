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
let BaseCardHeader = CardHeader
let BaseCardContent = CardContent
let BaseCardTitle = CardTitle

let CustomCard = withClickable(BaseCard)
let CustomCardHeader = withClickable(BaseCardHeader)
let CustomCardContent = withClickable(BaseCardContent)
let CustomCardTitle = withClickable(BaseCardTitle)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <CustomCard ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
      <CustomCardHeader uid={`${uid}-header`}>
        <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
      </CustomCardHeader>
      <CustomCardContent uid={`${uid}-content`}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </CustomCardContent>
    </CustomCard>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
