import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as BaseCard,
  CardContent as BaseCardContent,
  CardDescription as BaseCardDescription,
  CardFooter as BaseCardFooter,
  CardHeader as BaseCardHeader,
  CardTitle as BaseCardTitle,
} from "@/components/ui/card"

interface WithUid {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & WithUid>(
  ({ uid, ...props }, ref) => <BaseCard ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & WithUid>(
  ({ uid, ...props }, ref) => <BaseCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement> & WithUid>(
  ({ uid, ...props }, ref) => <BaseCardTitle ref={ref} {...props} />
)

let CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement> & WithUid>(
  ({ uid, ...props }, ref) => <BaseCardDescription ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & WithUid>(
  ({ uid, ...props }, ref) => <BaseCardContent ref={ref} {...props} />
)

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardDescription = withClickable(CardDescription)
CardContent = withClickable(CardContent)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => (
    <Card uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
      <CardHeader uid={`${uid}-header`}>
        <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        <CardDescription uid={`${uid}-desc`}>HP: {hp}/{maxHp}</CardDescription>
      </CardHeader>
      <CardContent uid={`${uid}-content`}>
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-contain"
        />
      </CardContent>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
