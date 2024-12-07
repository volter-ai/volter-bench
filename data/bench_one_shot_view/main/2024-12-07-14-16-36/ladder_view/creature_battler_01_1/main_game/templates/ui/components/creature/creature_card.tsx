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

interface BaseProps {
  uid: string
}

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement>, BaseProps {
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

let CreatureCardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ className, uid, ...props }, ref) => (
    <CardFooter ref={ref} className={className} {...props} />
  )
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement> & BaseProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let CreatureCardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement> & BaseProps>(
  ({ className, uid, ...props }, ref) => (
    <CardDescription ref={ref} className={className} {...props} />
  )
)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card ref={ref} className={cn("w-[350px]", className)} {...props}>
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
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardContent.displayName = "CreatureCardContent"
CreatureCardFooter.displayName = "CreatureCardFooter"
CreatureCardTitle.displayName = "CreatureCardTitle"
CreatureCardDescription.displayName = "CreatureCardDescription"

CreatureCard = withClickable(CreatureCard)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardContent = withClickable(CreatureCardContent)
CreatureCardFooter = withClickable(CreatureCardFooter)
CreatureCardTitle = withClickable(CreatureCardTitle)
CreatureCardDescription = withClickable(CreatureCardDescription)

export { 
  CreatureCard,
  CreatureCardHeader,
  CreatureCardContent,
  CreatureCardFooter,
  CreatureCardTitle,
  CreatureCardDescription
}
