import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardHeader as ShadcnCardHeader,
  CardTitle as ShadcnCardTitle,
  CardContent as ShadcnCardContent,
} from "@/components/ui/card"

interface PlayerCardProps extends React.ComponentProps<typeof ShadcnCard> {
  uid: string
  name: string
  imageUrl: string
}

let Card = withClickable(ShadcnCard)
let CardHeader = withClickable(ShadcnCardHeader)
let CardTitle = withClickable(ShadcnCardTitle)
let CardContent = withClickable(ShadcnCardContent)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
      <CardHeader uid={uid}>
        <CardTitle uid={uid}>{name}</CardTitle>
      </CardHeader>
      <CardContent uid={uid}>
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
