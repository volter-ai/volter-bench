import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent
} from "@/components/ui/card"

interface BaseProps {
  uid: string
}

interface PlayerCardProps extends React.ComponentProps<typeof Card>, BaseProps {
  name: string
  imageUrl: string
}

interface SubComponentProps extends React.HTMLAttributes<HTMLDivElement>, BaseProps {}

let PlayerCardHeader = React.forwardRef<HTMLDivElement, SubComponentProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let PlayerCardTitle = React.forwardRef<HTMLParagraphElement, SubComponentProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let PlayerCardContent = React.forwardRef<HTMLDivElement, SubComponentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[300px]", className)} {...props}>
      <PlayerCardHeader uid={`${uid}-header`}>
        <PlayerCardTitle uid={`${uid}-title`}>{name}</PlayerCardTitle>
      </PlayerCardHeader>
      <PlayerCardContent uid={`${uid}-content`}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </PlayerCardContent>
    </Card>
  )
)

PlayerCardHeader.displayName = "PlayerCardHeader"
PlayerCardTitle.displayName = "PlayerCardTitle"
PlayerCardContent.displayName = "PlayerCardContent"
PlayerCard.displayName = "PlayerCard"

PlayerCardHeader = withClickable(PlayerCardHeader)
PlayerCardTitle = withClickable(PlayerCardTitle)
PlayerCardContent = withClickable(PlayerCardContent)
PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
