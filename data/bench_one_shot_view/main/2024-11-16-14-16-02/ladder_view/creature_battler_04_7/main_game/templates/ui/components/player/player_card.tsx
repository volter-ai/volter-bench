import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as BaseCard,
  CardContent as BaseCardContent,
  CardHeader as BaseCardHeader,
  CardTitle as BaseCardTitle,
} from "@/components/ui/card"

interface PlayerCardProps extends React.ComponentProps<typeof BaseCard> {
  uid: string
  name: string
  imageUrl: string
}

let Card = withClickable(BaseCard)
let CardContent = withClickable(BaseCardContent)
let CardHeader = withClickable(BaseCardHeader)
let CardTitle = withClickable(BaseCardTitle)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
      <CardHeader uid={`${uid}-header`}>
        <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
      </CardHeader>
      <CardContent uid={`${uid}-content`}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </CardContent>
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
