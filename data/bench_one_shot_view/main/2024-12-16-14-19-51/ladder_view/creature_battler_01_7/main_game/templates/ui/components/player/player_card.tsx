import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as BaseCard,
  CardContent as BaseCardContent,
  CardHeader as BaseCardHeader,
  CardTitle as BaseCardTitle,
} from "@/components/ui/card"

interface WithUid {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof BaseCard> & WithUid>(
  ({ uid, ...props }, ref) => <BaseCard ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof BaseCardContent> & WithUid>(
  ({ uid, ...props }, ref) => <BaseCardContent ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof BaseCardHeader> & WithUid>(
  ({ uid, ...props }, ref) => <BaseCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, React.ComponentProps<typeof BaseCardTitle> & WithUid>(
  ({ uid, ...props }, ref) => <BaseCardTitle ref={ref} {...props} />
)

Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
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
