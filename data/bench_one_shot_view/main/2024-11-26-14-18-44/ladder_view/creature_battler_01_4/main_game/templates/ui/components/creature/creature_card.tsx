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

let Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
)

let CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardDescription ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
)

let CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardFooter ref={ref} {...props} />
)

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
      <Card uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
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

Card.displayName = "Card"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
CardDescription.displayName = "CardDescription"
CardContent.displayName = "CardContent"
CardFooter.displayName = "CardFooter"
CreatureCard.displayName = "CreatureCard"

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardDescription = withClickable(CardDescription)
CardContent = withClickable(CardContent)
CardFooter = withClickable(CardFooter)
CreatureCard = withClickable(CreatureCard)

export { CreatureCard, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter }
