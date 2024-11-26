import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface CreatureCardProps extends BaseCardProps {
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCardRoot = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} {...props} />
  )
)

let CreatureCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let CreatureCardDescription = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardDescription ref={ref} className={className} {...props} />
  )
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

let CreatureCardFooter = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardFooter ref={ref} className={className} {...props} />
  )
)

CreatureCardRoot.displayName = "CreatureCardRoot"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardTitle.displayName = "CreatureCardTitle"
CreatureCardDescription.displayName = "CreatureCardDescription"
CreatureCardContent.displayName = "CreatureCardContent"
CreatureCardFooter.displayName = "CreatureCardFooter"

CreatureCardRoot = withClickable(CreatureCardRoot)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardTitle = withClickable(CreatureCardTitle)
CreatureCardDescription = withClickable(CreatureCardDescription)
CreatureCardContent = withClickable(CreatureCardContent)
CreatureCardFooter = withClickable(CreatureCardFooter)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <CreatureCardRoot uid={`${uid}-root`} ref={ref} className={className} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
          <CreatureCardDescription uid={`${uid}-description`}>HP: {hp}/{maxHp}</CreatureCardDescription>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`}>
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-cover rounded-md"
          />
        </CreatureCardContent>
        <CreatureCardFooter uid={`${uid}-footer`} className="flex justify-between">
        </CreatureCardFooter>
      </CreatureCardRoot>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
