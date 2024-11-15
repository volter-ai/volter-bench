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

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={cn("w-[350px]", className)} {...props} />
  )
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

let BaseCardFooter = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardFooter ref={ref} className={className} {...props} />
  )
)

let BaseCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let BaseCardDescription = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardDescription ref={ref} className={className} {...props} />
  )
)

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardContent = withClickable(BaseCardContent)
BaseCardFooter = withClickable(BaseCardFooter)
BaseCardTitle = withClickable(BaseCardTitle)
BaseCardDescription = withClickable(BaseCardDescription)

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
      <BaseCard ref={ref} uid={uid} className={cn("w-[350px]", className)} {...props}>
        <BaseCardHeader uid={`${uid}-header`}>
          <BaseCardTitle uid={`${uid}-title`}>{name}</BaseCardTitle>
          <BaseCardDescription uid={`${uid}-description`}>HP: {hp}/{maxHp}</BaseCardDescription>
        </BaseCardHeader>
        <BaseCardContent uid={`${uid}-content`}>
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-cover rounded-md"
          />
        </BaseCardContent>
        <BaseCardFooter uid={`${uid}-footer`} className="flex justify-between">
        </BaseCardFooter>
      </BaseCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
