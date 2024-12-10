import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardContent as ShadcnCardContent,
  CardDescription as ShadcnCardDescription,
  CardFooter as ShadcnCardFooter,
  CardHeader as ShadcnCardHeader,
  CardTitle as ShadcnCardTitle,
} from "@/components/ui/card"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<
  HTMLDivElement, 
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCard {...props} ref={ref} uid={uid} />
))

let CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardHeader {...props} ref={ref} uid={uid} />
))

let CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardTitle {...props} ref={ref} uid={uid} />
))

let CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardDescription {...props} ref={ref} uid={uid} />
))

let CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardContent {...props} ref={ref} uid={uid} />
))

let CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseProps
>(({ uid, ...props }, ref) => (
  <ShadcnCardFooter {...props} ref={ref} uid={uid} />
))

Card.displayName = "Card"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
CardDescription.displayName = "CardDescription"
CardContent.displayName = "CardContent"
CardFooter.displayName = "CardFooter"

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardDescription = withClickable(CardDescription)
CardContent = withClickable(CardContent)
CardFooter = withClickable(CardFooter)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
        <CardHeader uid={uid}>
          <CardTitle uid={uid}>{name}</CardTitle>
          <CardDescription uid={uid}>HP: {hp}/{maxHp}</CardDescription>
        </CardHeader>
        <CardContent uid={uid}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-cover rounded-md"
          />
        </CardContent>
        <CardFooter uid={uid} className="flex justify-between">
        </CardFooter>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
