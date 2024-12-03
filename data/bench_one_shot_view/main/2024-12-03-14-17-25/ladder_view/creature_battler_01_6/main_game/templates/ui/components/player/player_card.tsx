import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
  CardDescription
} from "@/components/ui/card"

interface PlayerCardProps extends React.ComponentProps<typeof Card> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(({ className, uid, name, imageUrl, ...props }, ref) => (
  <Card ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
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
))

let PlayerCardHeader = withClickable(CardHeader)
let PlayerCardTitle = withClickable(CardTitle)
let PlayerCardDescription = withClickable(CardDescription)
let PlayerCardContent = withClickable(CardContent)
let PlayerCardFooter = withClickable(CardFooter)

PlayerCard.displayName = "PlayerCard"
PlayerCard = withClickable(PlayerCard)

export {
  PlayerCard,
  PlayerCardHeader,
  PlayerCardTitle,
  PlayerCardDescription,
  PlayerCardContent,
  PlayerCardFooter
}
