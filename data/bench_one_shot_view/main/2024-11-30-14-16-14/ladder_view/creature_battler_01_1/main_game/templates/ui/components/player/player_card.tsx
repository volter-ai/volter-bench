import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardHeader as ShadcnCardHeader,
  CardContent as ShadcnCardContent,
  CardFooter as ShadcnCardFooter,
  CardTitle as ShadcnCardTitle,
} from "@/components/ui/card"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>((props, ref) => <ShadcnCard {...props} ref={ref} />)

let CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>((props, ref) => <ShadcnCardHeader {...props} ref={ref} />)

let CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>((props, ref) => <ShadcnCardContent {...props} ref={ref} />)

let CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>((props, ref) => <ShadcnCardFooter {...props} ref={ref} />)

let CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement> & BaseProps
>((props, ref) => <ShadcnCardTitle {...props} ref={ref} />)

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardContent = withClickable(CardContent)
CardFooter = withClickable(CardFooter)
CardTitle = withClickable(CardTitle)

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

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
      <CardFooter uid={uid} className="flex justify-between" />
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
